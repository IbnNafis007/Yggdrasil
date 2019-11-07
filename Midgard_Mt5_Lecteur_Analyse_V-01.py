#usr/bin/env python
#-*-conding:utf8-*-


"""

# @author: Azazel                                                                      
*******************************************************************************************************
	
	Recupération des donné sour forme de ticks pour Machine Learning 
	On Recupère sur la periode DE 2000 Jusqu'à aujourd'hui 


	Script de création du prix médian , ainsi que les bougies OHLC en fonction du temps 
	Le fichier recupéré sont du style :

	      - Symbole        
	        ==========================================================================================
	        time      			      bid      ask     last   volume  flags

	        2018-07-31 00:05:02.708  0.89102  0.89130   0.0     0.0    134
	        2018-07-31 00:05:06.159  0.89093  0.89141   0.0     0.0    134
	        2018-07-31 00:05:07.516  0.89103  0.89130   0.0     0.0    134
	        2018-07-31 00:05:07.944  0.89102  0.89133   0.0     0.0    134
	
	medium_price=(ask+bid)/2 
	Bougie = [(t=60s){prix medium}]

"""

# import pour donné sur le système 
import os
import sys


# import pour Datascience et manipulation des stocks sous forme de DataFrame
import pandas as pd 
import numpy as np
import talib

# import pour la gestion  du temps 
from datetime import datetime
import pytz

# import pour La visualisation 
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import plt
plt.style.use('seaborn')

#import pour Metatrader5 et inter-action
from MetaTrader5 import *


#************************************ Varriables Immuable des symbole a trader *****************************************

ratios = ['EURUSD','GBPUSD','USDJPY','USDCHF','AUDUSD','GBPJPY','USDCAD','AUDCHF','AUDJPY','AUDNZD','CADCHF','CADJPY','CHFJPY','EURAUD','EURCAD','EURCHF','AUDCAD','EURGBP','NZDUSD','EURJPY','EURNZD','GBPAUD','GBPCHF','GBPJPY','GBPNZD','NZDCAD','NZDCHF','NZDJPY','EURPLN','EURHUF','USDCNH','USDRON','USNPLN','EURRUB','EURCZK','USDCZK','USDRUB','ASX200','CAC40','Canada60','DAX30','DJ30','FTSE100','HSCEI50','HSI50','AEX25','IBEX35','TECDAX30','JP225','MDAX30','NQ100','OBX25','SMI20','SP500','STOXX50','SouthAfrica40','SILVER','GOLD','COPPER','PALLADIUM','PLATINUM','BRENT','NGAS','WTI','COCOA','COTTON','ARABICA','ORANGE.JUICE','SUGAR.WHITE','ROBUSTA','SUGAR.RAW','EURHKD','EURHRK','EURNOK','EURRON','EURSEK','GBPCZK','GBPGBX','GBPPLN','GBPSGD','GBXUSD','USDARS','USDBGN','USDCLP','USDCOP','USDCRC','USDDKK','EURDKK','USDECS','USDX','USDGHS','USDHKD','USDHRK','USDHUF','USDIDR','USDKES','USDLAK','USDMMK','USDMXN','USDNOK','USDSEK','USDTZS','USDUAH','USDUAH','USDUGX','USDUSX','EURX','#BNK','#BNKE','#C50','#CEUG','#CMU','#AEEM','#ERO','#USA','#LEM','#MEU','#STZP','#TPXH','#DBXD','#EL4A','#EXS1','#IEMM','#IJPA','#IDVY','#VEUR','#VERX','#LYXIB','#CSSLI','#CSSMI','#CSSMIM',"#CHSPI",'#SMICHA','#XSMI','#SPICHA','#UKCHBH','#EUE','#IEMB','#IFF','#IHYU','#ISF','#IUKP','#IUSA','#IWDP','#L100','#MIDDL','#EMIM','#SEML','#IWDAU','#SJPA','#SLXX','#SWDA','#VMID','#VUKE','#VUSA','#XESC','#XESX','#XMEM', 'ACKB','#AEDEU','#AGFB','#AGS','#ARGX','#BAR','#BCART','#BEFB','#BEKB','#BPOST','#BPOST','#CFEB','#COFB','#COLR','#CYAD','#DIE','#ECONB','#ELI1','#EURN','#EVS','#FAGR','#GBLB','#ABI','#GIMP','#WDP','#GREEN','#IBAB','#INTO','#KBC','#KBCA','#KIN','#LOTB','#MELE','#NYR','#OBEL','#PROX','#REC1','#RET','#SIP','#SOF','#SOLB','#TESB','#UCB','#UMI','#UMI','#VAN','#ALMB','#AMBUB','#BO','#CARL.B','#CHR','#COLO.B','#DANSKE','#DENERG','#DFDS','#GEN','#GN','#ISS','#JYPK','#LUN','#ALAK.B','#MAERSK.A','#ZAL','#NKT','#NOVO.B','#NZYM.B','#PAAL.B','#PNDOR','#RBREW','#RILBA','#ROCK.B','#SCHO','#SIM','#SPNO','#STG','#SYDB','#TOP','#TRYG','#VWS']
#*********************************************************************************************************************
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2000, 1, 1, tzinfo=timezone)
UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
datas_directory = "./datas/"
ticks_directory = datas_directory + "ticks/"
bar = 100000
pathBourse = None




#***************************************** Definition pour Operation Système ******************************************




#****************************************** Definition pour Connection ***********************************************
def mt_connexion():
	MT5Initialize()			
	MT5WaitForTerminal()	

	if True: 
	    print("\t\t\t- Vous etes Connecter")
	    print("\t\t\t\t- Votre Compte est Le : " , MT5TerminalInfo())
	    print("\t\t\t\t- Votre Version de Metatrader est : ", MT5Version())
	else: 
	    print("Error Déconnection")
	    MT5Shutdown()
	    if True: 
	        print("Vous ete deconnecter")
	    else: 
	        print("Error")
	        MT5Shutdown()
	    sys.exit()


def mt_close():
	MT5Shutdown()
	if True:
		print('=' * 90, "\n\n\tVous etes deconnecter\n\n", '=' * 90)

	else: 
	    print('=' * 90, "\n\n\tError")
	    sys.exit(-10)



def display_dataframe(dataframe):
	print('=' * 90)
	print(dataframe)
	print('=' * 90)


def classement(ticks):
	ticks_frame = pd.DataFrame(list(ticks), 
						columns=['time', 'bid', 'ask', 'last', 'volume', 'flags'],)
	ticks_frame['time'] = ticks_frame.apply(lambda tick: local_to_utc(tick['time']), axis=1)
	 

	return ticks_frame.head(10)

def ticks(item, bar):
	global utc_from
	ticks = MT5CopyTicksFrom(item, utc_from, bar, MT5_COPY_TICKS_ALL)
	MT5WaitForTerminal()	# Attente de recuperation du terminal
	#print("Ticks received:",len(ticks))
	# shut down connection to MetaTrader 5
	MT5Shutdown()

	ticks_frame = pd.DataFrame(list(ticks), columns=['time', 'bid', 'ask', 'last', 'volume', 'flags'],)
	ticks_frame['time'] = ticks_frame.apply(lambda tick: local_to_utc(tick['time']), axis=1)


	return ticks_frame.head(10)

def local_to_utc(dt):
	global UTC_OFFSET_TIMEDELTA

	return dt + UTC_OFFSET_TIMEDELTA


def s():
	sys.exit()


#****************************************** Definition pour Analyse ***********************************************
def Analyse_Chartisme(dataframe):

	path = "./Analyse_Chartisme/"
	if not os.path.exists(path):
		os.makedirs(path)
	if os.path.exists(path):
		pass

	dataset = f'./Data_fxcm/{ratio}.csv'
	df = pd.read_csv(dataset, parse_dates=True)

	data = pd.DataFrame(df[['BidClose','AskClose']].mean(axis=1))
	# Feature Preparation 

	data['returns'] = np.log(data / data.shift(1))
	lags = 10
	cols = []
	for lag in range(1, lags+1):
		col = 'lag_%s' % lag
		data[col] = data['returns'].shift(lag)
		cols.append(col)
	data.dropna(inplace=True)
	print(data.info(),"\n" ,data.head(10))

	# support vecteur machine
	model = svm.SVC(C=1000)

	model.fit(np.sign(data[cols]), np.sign(data['returns']))
	pred = model.predict(np.sign(data[cols]))
	pred[:15]
	# Vectoriz Backteste
	data['position'] = pred
	data['strategy'] = data['position']* data['returns']
	# affichage sans levrage et spread
	data[['returns', 'strategy']].cumsum().apply(np.exp).plot()
	print(data['position'].value_counts())
	print(data['position'].diff().value_counts())
	print(data.info(), data.head())
	data.to_csv(f'Analyse_Chartisme/Chartisme_{ratio}.csv')

	return


def EWM(dataframe):
	# Ajout Exponentiel MV
	for i in np.arange(0.1, 1, 0.1):
		df[f'{ratio}_EWM-{i}'] = df[f'{ratio}_CloseMid'].ewm(alpha=i).mean()#.plot(figsize=(10, 6), lw=0.8, title=f'{ratio}')
	return

def patern(dataframe):
	"""
	Pattern Recognition:
	CDL2CROWS            Two Crows
	CDL3BLACKCROWS       Three Black Crows
	CDL3INSIDE           Three Inside Up/Down
	CDL3LINESTRIKE       Three-Line Strike
	CDL3OUTSIDE          Three Outside Up/Down
	CDL3STARSINSOUTH     Three Stars In The South
	CDL3WHITESOLDIERS    Three Advancing White Soldiers
	CDLABANDONEDBABY     Abandoned Baby
	CDLADVANCEBLOCK      Advance Block
	CDLBELTHOLD          Belt-hold
	CDLBREAKAWAY         Breakaway
	CDLCLOSINGMARUBOZU   Closing Marubozu
	CDLCONCEALBABYSWALL  Concealing Baby SwalLow
	CDLCOUNTERATTACK     Counterattack
	CDLDARKCLOUDCOVER    Dark Cloud Cover
	CDLDOJI              Doji
	CDLDOJISTAR          Doji Star
	CDLDRAGONFLYDOJI     Dragonfly Doji
	CDLENGULFING         Engulfing Pattern
	CDLEVENINGDOJISTAR   Evening Doji Star
	CDLEVENINGSTAR       Evening Star
	CDLGAPSIDESIDEWHITE  Up/Down-gap side-by-side white lines
	CDLGRAVESTONEDOJI    Gravestone Doji
	CDLHAMMER            Hammer
	CDLHANGINGMAN        Hanging Man
	CDLHARAMI            Harami Pattern
	CDLHARAMICROSS       Harami Cross Pattern
	CDLHighWAVE          High-Wave Candle
	CDLHIKKAKE           Hikkake Pattern
	CDLHIKKAKEMOD        Modified Hikkake Pattern
	CDLHOMINGPIGEON      Homing Pigeon
	CDLIDENTICAL3CROWS   Identical Three Crows
	CDLINNECK            In-Neck Pattern
	CDLINVERTEDHAMMER    Inverted Hammer
	CDLKICKING           Kicking
	CDLKICKINGBYLENGTH   Kicking - bull/bear determined by the longer marubozu
	CDLLADDERBOTTOM      Ladder Bottom
	CDLLONGLEGGEDDOJI    Long Legged Doji
	CDLLONGLINE          Long Line Candle
	CDLMARUBOZU          Marubozu
	CDLMATCHINGLow       Matching Low
	CDLMATHOLD           Mat Hold
	CDLMORNINGDOJISTAR   Morning Doji Star
	CDLMORNINGSTAR       Morning Star
	CDLONNECK            On-Neck Pattern
	CDLPIERCING          Piercing Pattern
	CDLRICKSHAWMAN       Rickshaw Man
	CDLRISEFALL3METHODS  Rising/Falling Three Methods
	CDLSEPARATINGLINES   Separating Lines
	CDLSHOOTINGSTAR      Shooting Star
	CDLSHORTLINE         Short Line Candle
	CDLSPINNINGTOP       Spinning Top
	CDLSTALLEDPATTERN    Stalled Pattern
	CDLSTICKSANDWICH     Stick Sandwich
	CDLTAKURI            Takuri (Dragonfly Doji with very long Lower shadow)
	CDLTASUKIGAP         Tasuki Gap
	CDLTHRUSTING         Thrusting Pattern
	CDLTRISTAR           Tristar Pattern
	CDLUNIQUE3RIVER      Unique 3 River
	CDLUPSIDEGAP2CROWS   Upside Gap Two Crows
	CDLXSIDEGAP3METHODS  Upside/Downside Gap Three Methods

	"""

	#CDL2CROWS - Two Crows
	df[f'{ratio}_CDL2CROWS'] = talib.CDL2CROWS(Open,High, Low, Close)
	#CDL2CROWS - Three Black Crows
	df[f'{ratio}_CDL2CROWS'] = talib.CDL3BLACKCROWS(Open,High, Low, Close)
	#CDL3INSIDE - Three Inside Up/Down
	df[f'{ratio}_CDL3INSIDE'] = talib.CDL3INSIDE(Open,High, Low, Close)
	#CDL3LINESTRIKE - Three-Line Strike
	df[f'{ratio}_CDL3LINESTRIKE'] = talib.CDL3LINESTRIKE(Open,High, Low, Close)
	#CDL3OUTSIDE - Three Outside Up/Down
	df[f'{ratio}_CDL3OUTSIDE'] = talib.CDL3OUTSIDE(Open,High, Low, Close)
	#CDL3STARSINSOUTH - Three Stars In The South
	df[f'{ratio}_CDL3STARSINSOUTH'] = talib.CDL3STARSINSOUTH(Open,High, Low, Close)
	#CDL3WHITESOLDIERS - Three Advancing White Soldiers
	df[f'{ratio}_CDL3WHITESOLDIERS'] = talib.CDL3WHITESOLDIERS(Open,High, Low, Close)
	#CDLABANDONEDBABY - Abandoned Baby
	df[f'{ratio}_CDLABANDONEDBABY'] = talib.CDLABANDONEDBABY(Open,High, Low, Close, penetration=0)
	#CDLADVANCEBLOCK - Advance Block
	df[f'{ratio}_CDLADVANCEBLOCK'] = talib.CDLADVANCEBLOCK(Open,High, Low, Close)
	#CDLBELTHOLD - Belt-hold
	df[f'{ratio}_CDLBELTHOLD'] = talib.CDLBELTHOLD(Open,High, Low, Close)
	#CDLBREAKAWAY - Breakaway
	df[f'{ratio}_CDLBREAKAWAY'] = talib.CDLBREAKAWAY(Open,High, Low, Close)
	#CDLCLOSINGMARUBOZU - Closing Marubozu
	df[f'{ratio}_CDLCLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(Open,High, Low, Close)
	#CDLCONCEALBABYSWALL - Concealing Baby SwalLow
	df[f'{ratio}_CDLCLOSINGMARUBOZU'] = talib.CDLCONCEALBABYSWALL(Open,High, Low, Close)
	#CDLCOUNTERATTACK - Counterattack
	df[f'{ratio}_CDLCLOSINGMARUBOZU'] = talib.CDLCOUNTERATTACK(Open,High, Low, Close)
	#CDLDARKCLOUDCOVER - Dark Cloud Cover
	df[f'{ratio}_CDLCLOSINGMARUBOZU'] = talib.CDLDARKCLOUDCOVER(Open,High, Low, Close, penetration=0)
	#CDLDOJI - Doji
	df[f'{ratio}_CDLDOJI'] = talib.CDLDOJI(Open,High, Low, Close)
	#CDLDOJISTAR - Doji Star
	df[f'{ratio}_CDLDOJISTAR'] = talib.CDLDOJISTAR(Open,High, Low, Close)
	#CDLDRAGONFLYDOJI - Dragonfly Doji
	df[f'{ratio}_CDLDRAGONFLYDOJI'] = talib.CDLDRAGONFLYDOJI(Open,High, Low, Close)
	#CDLENGULFING - Engulfing Pattern
	df[f'{ratio}_CDLENGULFING'] = talib.CDLENGULFING(Open,High, Low, Close)
	#CDLEVENINGDOJISTAR - Evening Doji Star
	df[f'{ratio}_CDLEVENINGDOJISTAR'] = talib.CDLEVENINGDOJISTAR(Open,High, Low, Close, penetration=0)
	#CDLEVENINGSTAR - Evening Star
	df[f'{ratio}_CDLEVENINGSTAR'] = talib.CDLEVENINGSTAR(Open,High, Low, Close, penetration=0)
	#CDLGAPSIDESIDEWHITE - Up/Down-gap side-by-side white lines
	df[f'{ratio}_CDLEVENINGSTAR'] = talib.CDLGAPSIDESIDEWHITE(Open,High, Low, Close)
	#CDLGRAVESTONEDOJI - Gravestone Doji
	df[f'{ratio}_CDLGRAVESTONEDOJI'] = talib.CDLGRAVESTONEDOJI(Open,High, Low, Close)
	#CDLHAMMER - Hammer
	df[f'{ratio}_CDLGRAVESTONEDOJI'] = talib.CDLHAMMER(Open,High, Low, Close)
	#CDLHANGINGMAN - Hanging Man
	df[f'{ratio}_CDLGRAVESTONEDOJI'] = talib.CDLHANGINGMAN(Open,High, Low, Close)
	#CDLHARAMI - Harami Pattern
	df[f'{ratio}_CDLGRAVESTONEDOJI'] = talib.CDLHARAMI(Open,High, Low, Close)
	#CDLHARAMICROSS - Harami Cross Pattern
	df[f'{ratio}_CDLHARAMICROSS'] = talib.CDLHARAMICROSS(Open,High, Low, Close)
	#CDLHighWAVE -High-Wave Candle
	#df[f'{ratio}_CDLHighWAVE'] = talib.CDLHighWAVE(Open,High, Low, Close)
	#CDLHIKKAKE - Hikkake Pattern
	df[f'{ratio}_CDLHIKKAKE'] = talib.CDLHIKKAKE(Open,High, Low, Close)
	#CDLHIKKAKEMOD - Modified Hikkake Pattern
	df[f'{ratio}_CDLHIKKAKEMOD'] = talib.CDLHIKKAKEMOD(Open,High, Low, Close)
	#CDLHOMINGPIGEON - Homing Pigeon
	df[f'{ratio}_CDLHOMINGPIGEON'] = talib.CDLHOMINGPIGEON(Open,High, Low, Close)
	#CDLIDENTICAL3CROWS - Identical Three Crows
	df[f'{ratio}_CDLIDENTICAL3CROWS'] = talib.CDLIDENTICAL3CROWS(Open,High, Low, Close)
	#CDLINNECK - In-Neck Pattern
	df[f'{ratio}_CDLINNECK'] = talib.CDLINNECK(Open,High, Low, Close)
	#CDLINVERTEDHAMMER - Inverted Hammer
	df[f'{ratio}_CDLINVERTEDHAMMER'] = talib.CDLINVERTEDHAMMER(Open,High, Low, Close)
	#CDLKICKING - Kicking
	df[f'{ratio}_CDLKICKING'] = talib.CDLKICKING(Open,High, Low, Close)
	#CDLKICKINGBYLENGTH - Kicking - bull/bear determined by the longer marubozu
	df[f'{ratio}_CDLKICKINGBYLENGTH'] = talib.CDLKICKINGBYLENGTH(Open,High, Low, Close)
	#CDLLADDERBOTTOM - Ladder Bottom
	df[f'{ratio}_CDLLADDERBOTTOM'] = talib.CDLLADDERBOTTOM(Open,High, Low, Close)
	#CDLLONGLEGGEDDOJI - Long Legged Doji
	df[f'{ratio}_CDLLONGLEGGEDDOJI'] = talib.CDLLONGLEGGEDDOJI(Open,High, Low, Close)
	#CDLLONGLINE - Long Line Candle
	df[f'{ratio}_CDLLONGLINE'] = talib.CDLLONGLINE(Open,High, Low, Close)
	#CDLMARUBOZU - Marubozu
	df[f'{ratio}_DLMARUBOZU'] = talib.CDLMARUBOZU(Open,High, Low, Close)
	#CDLMATCHINGLow - Matching Low
	#df[f'{ratio}_CDLMATCHINGLow'] = talib.CDLMATCHINGLow(Open,High, Low, Close)
	#CDLMATHOLD - Mat Hold
	df[f'{ratio}_CDLMATHOLD'] = talib.CDLMATHOLD(Open,High, Low, Close, penetration=0)
	#CDLMORNINGDOJISTAR - Morning Doji Star
	df[f'{ratio}_CDLMORNINGDOJISTAR'] = talib.CDLMORNINGDOJISTAR(Open,High, Low, Close, penetration=0)
	#CDLMORNINGSTAR - Morning Star
	df[f'{ratio}_CDLMORNINGSTAR'] = talib.CDLMORNINGSTAR(Open,High, Low, Close, penetration=0)
	#CDLONNECK - On-Neck Pattern
	df[f'{ratio}_CDLONNECK'] = talib.CDLONNECK(Open,High, Low, Close)
	#CDLPIERCING - Piercing Pattern
	df[f'{ratio}_CDLPIERCING'] = talib.CDLPIERCING(Open,High, Low, Close)
	#CDLRICKSHAWMAN - Rickshaw Man
	df[f'{ratio}_CDLRICKSHAWMAN'] = talib.CDLRICKSHAWMAN(Open,High, Low, Close)
	#CDLRISEFALL3METHODS - Rising/Falling Three Methods
	df[f'{ratio}_CDLRISEFALL3METHODS'] = talib.CDLRISEFALL3METHODS(Open,High, Low, Close)
	#CDLSEPARATINGLINES - Separating Lines
	df[f'{ratio}_CDLSEPARATINGLINES'] = talib.CDLSEPARATINGLINES(Open,High, Low, Close)
	#CDLSHOOTINGSTAR - Shooting Star
	df[f'{ratio}_CDLSHOOTINGSTAR'] = talib.CDLSHOOTINGSTAR(Open,High, Low, Close)
	#CDLSHORTLINE - Short Line Candle
	df[f'{ratio}_CDLSHORTLINE'] = talib.CDLSHORTLINE(Open,High, Low, Close)
	#CDLSPINNINGTOP - Spinning Top
	df[f'{ratio}_CDLSPINNINGTOP'] = talib.CDLSPINNINGTOP(Open,High, Low, Close)
	#CDLSTALLEDPATTERN - Stalled Pattern
	df[f'{ratio}_CDLSTALLEDPATTERN'] = talib.CDLSTALLEDPATTERN(Open,High, Low, Close)
	#CDLSTICKSANDWICH - Stick Sandwich
	df[f'{ratio}_CDLSTICKSANDWICH'] = talib.CDLSTICKSANDWICH(Open,High, Low, Close)
	#CDLTAKURI - Takuri (Dragonfly Doji with very long Lower shadow)
	df[f'{ratio}_CDLTAKURI'] = talib.CDLTAKURI(Open,High, Low, Close)
	#CDLTASUKIGAP - Tasuki Gap
	df[f'{ratio}_CDLTASUKIGAP'] = talib.CDLTASUKIGAP(Open,High, Low, Close)
	#CDLTHRUSTING - Thrusting Pattern
	df[f'{ratio}_CDLTHRUSTING'] = talib.CDLTHRUSTING(Open,High, Low, Close)
	#CDLTRISTAR - Tristar Pattern
	df[f'{ratio}_CDLTRISTAR'] = talib.CDLTRISTAR(Open,High, Low, Close)
	#CDLUNIQUE3RIVER - Unique 3 River
	df[f'{ratio}_CDLUNIQUE3RIVER'] = talib.CDLUNIQUE3RIVER(Open,High, Low, Close)
	#CDLUPSIDEGAP2CROWS - Upside Gap Two Crows
	df[f'{ratio}_CDLUPSIDEGAP2CROWS'] = talib.CDLUPSIDEGAP2CROWS(Open,High, Low, Close)
	#CDLXSIDEGAP3METHODS - Upside/Downside Gap Three Methods
	df[f'{ratio}_CDLXSIDEGAP3METHODS'] = talib.CDLXSIDEGAP3METHODS(Open,High, Low, Close)

	return patern


def IndicateurTech(dataframe):
	"""

	Overlap Studies:

	BBANDS               Bollinger Bands
	DEMA                 Double Exponential Moving Average
	EMA                  Exponential Moving Average
	HT_TRENDLINE         Hilbert Transform - Instantaneous Trendline
	KAMA                 Kaufman Adaptive Moving Average
	MA                   Moving average
	MAMA                 MESA Adaptive Moving Average
	MAVP                 Moving average with variable period
	MIDPOINT             MidPoint over period
	MIDPRICE             Midpoint Price over period
	SAR                  Parabolic SAR
	SAREXT               Parabolic SAR - Extended
	SMA                  Simple Moving Average
	T3                   Triple Exponential Moving Average (T3)
	TEMA                 Triple Exponential Moving Average
	TRIMA                Triangular Moving Average
	WMA                  Weighted Moving Average

	"""

	# BBANDS - Bollinger Bands
	upperband, middleband, Lowerband = talib.BBANDS(Close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
	#DEMA - Double Exponential Moving Average
	df[f'{ratio}_DEMA'] = talib.DEMA(Close, timeperiod=30)
	#EMA - Exponential Moving Average
	#NOTE: The EMA function has an unstable period.
	df[f'{ratio}_EMA'] = talib.EMA(Close, timeperiod=30)
	#HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
	#NOTE: The HT_TRENDLINE function has an unstable period.
	df[f'{ratio}_HT_TRENDLINE'] = talib.HT_TRENDLINE(Close)
	#KAMA - Kaufman Adaptive Moving Average
	#NOTE: The KAMA function has an unstable period.
	df[f'{ratio}_KAMA'] = talib.KAMA(Close, timeperiod=30)
	#MA - Moving average
	df[f'{ratio}_MA'] = talib.MA(Close, timeperiod=30, matype=0)
	#MAMA - MESA Adaptive Moving Average
	#NOTE: The MAMA function has an unstable period.
	#mama, fama = talib.MAMA(Close, fastlimit=0, sLowlimit=0)
	#MAVP - Moving average with variable period
	#df[f'{ratio}_MAVP'] = talib.MAVP(Close, periods, minperiod=2, maxperiod=30, matype=0)
	#MIDPOINT - MidPoint over period
	df[f'{ratio}_MIDPOINT'] = talib.MIDPOINT(Close, timeperiod=14)
	#MIDPRICE - Midpoint Price over period
	df[f'{ratio}_MIDPRICE'] = talib.MIDPRICE(High, Low, timeperiod=14)
	#SAR - Parabolic SAR
	df[f'{ratio}_SAR'] = talib.SAR(High, Low, acceleration=0, maximum=0)
	#SAREXT - Parabolic SAR - Extended
	df[f'{ratio}_SAREXT'] = talib.SAREXT(High, Low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)
	#SMA - Simple Moving Average
	df[f'{ratio}_SMA'] = talib.SMA(Close, timeperiod=30)
	#T3 - Triple Exponential Moving Average (T3)
	#NOTE: The T3 function has an unstable period.
	df[f'{ratio}_T3'] = talib.T3(Close, timeperiod=5, vfactor=0)
	#TEMA - Triple Exponential Moving Average
	df[f'{ratio}_TEMA'] = talib.TEMA(Close, timeperiod=30)
	#TRIMA - Triangular Moving Average
	df[f'{ratio}_TRIMA'] = talib.TRIMA(Close, timeperiod=30)
	#WMA - Weighted Moving Average
	df[f'{ratio}_WMA'] = talib.WMA(Close, timeperiod=30)


def Momentum_Indicators(dataframe):
	"""
	Momentum Indicators:

	ADX                  Average Directional Movement Index
	ADXR                 Average Directional Movement Index Rating
	APO                  Absolute Price Oscillator
	AROON                Aroon
	AROONOSC             Aroon Oscillator
	BOP                  Balance Of Power
	CCI                  Commodity Channel Index
	CMO                  Chande Momentum Oscillator
	DX                   Directional Movement Index
	MACD                 Moving Average Convergence/Divergence
	MACDEXT              MACD with controllable MA type
	MACDFIX              Moving Average Convergence/Divergence Fix 12/26
	MFI                  Money FLow Index
	MINUS_DI             Minus Directional Indicator
	MINUS_DM             Minus Directional Movement
	MOM                  Momentum
	PLUS_DI              Plus Directional Indicator
	PLUS_DM              Plus Directional Movement
	PPO                  Percentage Price Oscillator
	ROC                  Rate of change : ((price/prevPrice)-1)*100
	ROCP                 Rate of change Percentage: (price-prevPrice)/prevPrice
	ROCR                 Rate of change ratio: (price/prevPrice)
	ROCR100              Rate of change ratio 100 scale: (price/prevPrice)*100
	RSI                  Relative Strength Index
	STOCH                Stochastic
	STOCHF               Stochastic Fast
	STOCHRSI             Stochastic Relative Strength Index
	TRIX                 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
	ULTOSC               Ultimate Oscillator
	WILLR                Williams' %R
	"""
	#ADX - Average Directional Movement Index
	df[f'{ratio}_ADX'] = talib.ADX(High, Low, Close, timeperiod=14)
	#ADXR - Average Directional Movement Index Rating
	df[f'{ratio}_ADXR'] = talib.ADXR(High, Low, Close, timeperiod=14)
	#APO - Absolute Price Oscillator
	#df[f'{ratio}_APO'] = talib.APO(Close, fastperiod=12, sLowperiod=26, matype=0)
	#AROON - Aroon
	aroondown, aroonup = talib.AROON(High, Low, timeperiod=14)
	#AROONOSC - Aroon Oscillator
	df[f'{ratio}_AROONOSC'] = talib.AROONOSC(High, Low, timeperiod=14)
	#BOP - Balance Of Power
	df[f'{ratio}_BOP'] = talib.BOP(Open, High, Low, Close)
	#CCI - Commodity Channel Index
	df[f'{ratio}_CCI'] = talib.CCI(High, Low, Close, timeperiod=14)
	#CMO - Chande Momentum Oscillator
	df[f'{ratio}_CMO'] = talib.CMO(Close, timeperiod=14)
	#DX - Directional Movement Index
	df[f'{ratio}_DX'] = talib.DX(High, Low, Close, timeperiod=14)
	
	#MACD - Moving Average Convergence/Divergence
	#macd, macdsignal, macdhist = talib.MACD(Close, fastperiod=12, sLowperiod=26, signalperiod=9)
	#MACDEXT - MACD with controllable MA type
	#macd, macdsignal, macdhist = talib.MACDEXT(Close, fastperiod=12, fastmatype=0, sLowperiod=26, sLowmatype=0, signalperiod=9, signalmatype=0)
	#MACDFIX - Moving Average Convergence/Divergence Fix 12/26
	#macd, macdsignal, macdhist = talib.MACDFIX(Close, signalperiod=9)
	#MFI - Money FLow Index
	#df[f'{ratio}_MFI'] = talib.MFI(High, Low, Close, volume, timeperiod=14)
	
	#MINUS_DI - Minus Directional Indicator
	df[f'{ratio}_MINUS_DI'] = talib.MINUS_DI(High, Low, Close, timeperiod=14) 
	#MINUS_DM - Minus Directional Movement
	df[f'{ratio}_MINUS_DM'] = talib.MINUS_DM(High, Low, timeperiod=14)
	#Minus Directional Movement 
	#MOM - Momentum
	df[f'{ratio}_MOM'] = talib.MOM(Close, timeperiod=10) 
	#PLUS_DI - Plus Directional Indicator
	df[f'{ratio}_PLUS_DI'] = talib.PLUS_DI(High, Low, Close, timeperiod=14)
	#PLUS_DM - Plus Directional Movement
	df[f'{ratio}_PLUS_DM'] = talib.PLUS_DM(High, Low, timeperiod=14) 
	
	#PPO - Percentage Price Oscillator
	#df[f'{ratio}_PPO'] = talib.PPO(Close, fastperiod=12, sLowperiod=26, matype=0)
	#ROC - Rate of change : ((price/prevPrice)-1)*100
	df[f'{ratio}_ROC'] = talib.ROC(Close, timeperiod=10)
	#ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
	df[f'{ratio}_ROCP'] = talib.ROCP(Close, timeperiod=10)
	#ROCR - Rate of change ratio: (price/prevPrice)
	df[f'{ratio}_ROCR'] = talib.ROCR(Close, timeperiod=10)
	#ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
	df[f'{ratio}_ROCR100'] = talib.ROCR100(Close, timeperiod=10)
	#RSI - Relative Strength Index
	#NOTE: The RSI function has an unstable period.
	df[f'{ratio}_RSI'] = talib.RSI(Close, timeperiod=14)
	
	#STOCH - Stochastic
	#sLowk, sLowd = talib.STOCH(High, Low, Close, fastk_period=5, sLowk_period=3, sLowk_matype=0, sLowd_period=3, sLowd_matype=0)
	#STOCHF - Stochastic Fast
	fastk, fastd = talib.STOCHF(High, Low, Close, fastk_period=5, fastd_period=3, fastd_matype=0)
	#STOCHRSI - Stochastic Relative Strength Index
	fastk, fastd = talib.STOCHRSI(Close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
	#TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
	df[f'{ratio}_TRIX'] = talib.TRIX(Close, timeperiod=30)
	#ULTOSC - Ultimate Oscillator
	df[f'{ratio}_ULTOSC'] = talib.ULTOSC(High, Low, Close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
	#WILLR - Williams' %R
	df[f'{ratio}_ULTOSC'] = talib.WILLR(High, Low, Close, timeperiod=14)

	return


def Cylcle_Indicators(dataframe):
	"""

	Cycle Indicators

	HT_DCPERIOD          Hilbert Transform - Dominant Cycle Period
	HT_DCPHASE           Hilbert Transform - Dominant Cycle Phase
	HT_PHASOR            Hilbert Transform - Phasor Components
	HT_SINE              Hilbert Transform - SineWave
	HT_TRENDMODE         Hilbert Transform - Trend vs Cycle Mode

	"""

	#Cycle Indicator Functions
	#HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period
	df[f'{ratio}_HT_DCPERIOD'] = talib.HT_DCPERIOD(Close)
	#HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase
	df[f'{ratio}_HT_DCPHASE'] = talib.HT_DCPHASE(Close)
	#HT_PHASOR - Hilbert Transform - Phasor Components
	inphase, quadrature = talib.HT_PHASOR(Close)
	#HT_SINE - Hilbert Transform - SineWave
	sine, leadsine = talib.HT_SINE(Close)
	#HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode
	integer = talib.HT_TRENDMODE(Close)

	return



def Price_Transform(dataframe):
	"""
	Price Transform

	AVGPRICE             Average Price
	MEDPRICE             Median Price
	TYPPRICE             Typical Price
	WCLPRICE             Weighted Close Price

	"""
	#Price Transform Functions
	#AVGPRICE - Average Price
	df[f'{ratio}_AVGPRICE'] = talib.AVGPRICE(Open, High, Low, Close)
	#MEDPRICE - Median Price
	df[f'{ratio}_MEDPRICE'] = talib.MEDPRICE(High, Low)
	#TYPPRICE - Typical Price
	df[f'{ratio}_TYPPRICE'] = talib.TYPPRICE(High, Low, Close)
	#WCLPRICE - Weighted Close Price
	df[f'{ratio}_WCLPRICE'] = talib.WCLPRICE(High, Low, Close)
	return


def Stat_Function(dataframe):
	#Statistic Functions
	#BETA - Beta
	df[f'{ratio}_BETA'] = talib.BETA(High, Low, timeperiod=5)
	#CORREL - Pearson's Correlation Coefficient (r)
	df[f'{ratio}_CORREL'] = talib.CORREL(High, Low, timeperiod=30)
	#LINEARREG - Linear Regression
	df[f'{ratio}_LINEARREG'] = talib.LINEARREG(Close, timeperiod=14)
	#LINEARREG_ANGLE - Linear Regression Angle
	df[f'{ratio}_LINEARREG_ANGLE'] = talib.LINEARREG_ANGLE(Close, timeperiod=14)
	#LINEARREG_INTERCEPT - Linear Regression Intercept
	df[f'{ratio}_LINEARREG_INTERCEPT'] = talib.LINEARREG_INTERCEPT(Close, timeperiod=14)
	#LINEARREG_SLOPE - Linear Regression Slope
	df[f'{ratio}_LINEARREG_SLOPE'] = talib.LINEARREG_SLOPE(Close, timeperiod=14)
	#STDDEV - Standard Deviation
	df[f'{ratio}_STDDEV'] = talib.STDDEV(Close, timeperiod=5, nbdev=1)
	#TSF - Time Series Forecast
	df[f'{ratio}_TSF'] = talib.TSF(Close, timeperiod=14)
	#VAR - Variance
	df[f'{ratio}_VAR'] = talib.VAR(Close, timeperiod=5, nbdev=1)

	return



def Math_Operators(dataframe):
	#Math Operator Functions
	#ADD - Vector Arithmetic Add
	df[f'{ratio}_ADD'] = talib.ADD(High, Low)
	#c - Vector Arithmetic Div
	df[f'{ratio}_ADD'] = talib.DIV(High, Low)
	#MAX - Highest value over a specified period
	df[f'{ratio}_MAX'] = talib.MAX(Close, timeperiod=30)
	#MAXINDEX - Index of Highest value over a specified period
	#integer = MAXINDEX(Close, timeperiod=30)
	#MIN - Lowest value over a specified period
	df[f'{ratio}_MIN'] = talib.MIN(Close, timeperiod=30)
	#MININDEX - Index of Lowest value over a specified period
	integer = talib.MININDEX(Close, timeperiod=30)
	#MINMAX - Lowest and Highest values over a specified period
	min, max = talib.MINMAX(Close, timeperiod=30)
	#MINMAXINDEX - Indexes of Lowest and Highest values over a specified period
	minidx, maxidx = talib.MINMAXINDEX(Close, timeperiod=30)
	#MULT - Vector Arithmetic Mult
	df[f'{ratio}_MULT'] = talib.MULT(High, Low)
	#SUB - Vector Arithmetic Substraction
	df[f'{ratio}_SUB'] = talib.SUB(High, Low)
	#SUM - Summation
	df[f'{ratio}_SUM'] = talib.SUM(Close, timeperiod=30)

	return

def Math_Transform(dataframe):
	#Math Transform Functions
	#ACOS - Vector Trigonometric ACos
	df[f'{ratio}_ACOS'] = talib.ACOS(Close)
	#ASIN - Vector Trigonometric ASin
	df[f'{ratio}_ASIN'] = talib.ASIN(Close)
	#ATAN - Vector Trigonometric ATan
	df[f'{ratio}_ATAN'] = talib.ATAN(Close)
	#CEIL - Vector Ceil
	df[f'{ratio}_CEIL'] = talib.CEIL(Close)
	#COS - Vector Trigonometric Cos
	df[f'{ratio}_COS'] = talib.COS(Close)
	#COSH - Vector Trigonometric Cosh
	df[f'{ratio}_COSH'] = talib.COSH(Close)
	#EXP - Vector Arithmetic Exp
	df[f'{ratio}_EXP'] = talib.EXP(Close)
	#FLOOR - Vector Floor
	df[f'{ratio}_FLOOR'] = talib.FLOOR(Close)
	#LN - Vector Log Natural
	df[f'{ratio}_LN'] = talib.LN(Close)
	#LOG10 - Vector Log10
	df[f'{ratio}_LOG10'] = talib.LOG10(Close)
	#SIN - Vector Trigonometric Sin
	df[f'{ratio}_SIN'] = talib.SIN(Close)
	#SINH - Vector Trigonometric Sinh
	df[f'{ratio}_SINH'] = talib.SINH(Close)
	#SQRT - Vector Square Root
	df[f'{ratio}_SQRT'] = talib.SQRT(Close)
	#TAN - Vector Trigonometric Tan
	df[f'{ratio}_TAN'] = talib.TAN(Close)
	#TANH - Vector Trigonometric Tanh
	df[f'{ratio}_TANH'] = talib.TANH(Close)

	return


def normalise(dataframe):

	df.rename(columns={"BidOpen": f"{ratio}_BidOpen", "BidHigh": f"{ratio}_BidHigh", "BidLow": f"{ratio}_BidLow", "BidClose": f"{ratio}_BidClose" , "AskOpen": f"{ratio}_AskOpen", "AskHigh": f"{ratio}_AskHigh", "AskLow": f"{ratio}_AskLow", "AskClose": f"{ratio}_AskClose"}, inplace=True)

	df[f'{ratio}_OpenMid'] = df[[f'{ratio}_AskOpen',f'{ratio}_BidOpen']].mean(axis=1)
	df[f'{ratio}_HighMid'] = df[[f'{ratio}_AskHigh',f'{ratio}_BidHigh']].mean(axis=1)
	df[f'{ratio}_LowMid'] = df[[f'{ratio}_AskHigh',f'{ratio}_BidLow']].mean(axis=1)
	df[f'{ratio}_CloseMid'] = df[[f'{ratio}_AskClose',f'{ratio}_BidClose']].mean(axis=1)
	return
#*********************************************************************************************

if __name__ == '__main__':
	main_df = pd.DataFrame()

	try:
		print("/+++/"*30,'\n\n\t',"Nous Navons pas d'érreur dans le boucle principale au lancement ! \n")

		try:
			
			#for ratio in ratios:
				mt_connexion()
				dataframe = ticks(ratio, bar)
				display_dataframe(dataframe)
				path = "./Analyse_csv/"
				if not os.path.exists(path):
					os.makedirs(path)
				if os.path.exists(path):
					pass
			#	dataframe.to_csv(f'{ratio}.csv')
			#	mt_close()

			#	sys.exit()


			for ratio in ratios:
				df = pd.read_csv(path,f"{ratio}.csv")
				normalise(df)
				EWM(df)
				IndicateurTech(df)
				display_dataframe(df)
				Momentum_Indicators(df)
				sys.exit()
		except :
			print("/+++/"*30,'\n\n\t'," Error etape  Connextion\n\n")
			#mt_close()
			pass
	

	if len(main_df) == 0:
		main_df = df
	else:
		pass
		main_df = main_df.join(df)

	except :
		print("/+++/"*30,'\n\n\t'," Error in __main__ \n\n")
		#sys.exit()
