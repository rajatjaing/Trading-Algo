from datetime import date,timedelta
from nsepy import get_history
import talib
import csv
import pandas as pd
import smtplib,ssl
from collections import OrderedDict
from nsetools import Nse
import numpy as np
from pprint import pprint
from yahoo_fin.stock_info import get_live_price




MsgNormalArray=[]
MsgBuyArray=[]
MsgSellArray=[]
nifty50Array=[]

Today = date.today()
Start=date(2018,1,1)
yesterday = Today - timedelta(days = 1)
tomorrow=Today + timedelta(days = 1)
print("Today's Date : "+str(Today))
print("Yesterday's Date : "+str(yesterday))
print("tomorrow's Date : "+str(tomorrow))


# http://theautomatic.net/yahoo_fin-documentation/#get_data

# nifty50Array=['ADANIPORTS','ASIANPAINT','AXISBANK','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BPCL','BHARTIARTL','INFRATEL','BRITANNIA','CIPLA',
# 'COALINDIA','DRREDDY','EICHERMOT','GAIL','GRASIM','HCLTECH','HDFCBANK','HEROMOTOCO','HINDALCO','HINDUNILVR','HDFC','ICICIBANK','ITC','IBULHSGFIN','IOC','INDUSINDBK','INFY','JSWSTEEL','KOTAKBANK','LT','M&M','MARUTI','NTPC','ONGC','POWERGRID','RELIANCE','SBIN','SUNPHARMA','TCS','TATAMOTORS','TATASTEEL','TECHM','TITAN',
# 'UPL','ULTRACEMCO','VEDL','WIPRO','YESBANK','ZEEL']


nifty50Array=['SBIN']

#----------------------------------------------------------------------------top_gainers-------------------------------------------------------------------------
nse = Nse()
top_gainers = nse.get_top_gainers()
df=pd.DataFrame(top_gainers)
#print (df['symbol'])
# print (df['highPrice'])
#print(df)
# for index,row in df.iterrows():
 # print(row['symbol'])
 # SYMBOL=row['symbol']

#----------------------------------------------------------------------------Stock quote live--------------------------------------------------------------------
 
 
 
qoutes = nse.get_quote('TATAMOTORS')
#pprint(qoutes)
for key,value in qoutes.items():
 if key=='dayHigh':
     print("day high : "+str("%.2f" % value))
 if key=='dayLow':
     print("day Low : "+str("%.2f" % value))
 if key=='open':
	 print("day open : " +str("%.2f" % value))
 if key=='closePrice':
     print("day close : "+str("%.2f" % value))
 if key=='previousClose':
     print("previous day close : "+str("%.2f" % value))


# current_price=get_live_price('TATAMOTORS.NS')
# print("current price : "+str("%.2f" % current_price))	 


 
 
 
 
 
 
 
for SYMBOL in nifty50Array:




 
 #-----------------------------------------------------------------------Pivot points-----------------------------------------------------------------------------
 pnb=get_history(symbol=SYMBOL,start=Start,end=Today)
 yesterday_close=pnb['Close']
 yesterday_open=pnb['Open']
 yesterday_high=pnb['High']
 yesterday_low=pnb['Low']
 # print(type(yesterday_close))
 yOpen=yesterday_open.values.tolist()[0]
 yClose=yesterday_close.values.tolist()[0]
 yHigh=yesterday_high.values.tolist()[0]
 yLow=yesterday_low.values.tolist()[0]
 
 print('yetsterday open : '+str(yOpen))
 print('yetsterday High : '+str(yHigh))
 print('yetsterday low : '+str(yLow))
 print('yetsterday close : '+str(yClose))
 
 #pivot point calculation

 PP = (yHigh+yLow+yClose) / 3
 print("pivot point :"+str("%.2f" % PP))
 
 #First level support and resistance:
 R1 = (2*PP)-yLow
 S1 = (2*PP)-yHigh
# Second level of support and resistance:
 R2 = PP+(yHigh-yLow)
 S2 = PP-(yHigh-yLow)
# Third level of support and resistance:
 R3 = yHigh+2*(PP-yLow)
 S3 = yLow-2*(yHigh-PP)


 print("support level 1 :" + str("%.2f" % S1))
 print("support level 2 :" + str("%.2f" % S2))
 print("support level 3 :" + str("%.2f" % S3))

 print("resistance level 1 :" + str("%.2f" % R1))
 print("resistance level 2 :" + str("%.2f" % R2))
 print("resistance level 3 :" + str("%.2f" % R3))
 
 
#-------------------------------------------------------------------------------RSI indicator--------------------------------------------------------
 
 
 sbin= get_history(symbol=SYMBOL,start=Start,end=tomorrow)
 Close_value=sbin['Close']
 High_value=sbin['High']
 Low_value=sbin['Low']
 #print Close_value
 
 rsi_data = talib.RSI(Close_value,timeperiod =14) 
 s=pd.DataFrame({'date':rsi_data.index,'RSI':rsi_data.values})
# print(s)
 rsi=s["RSI"].iloc[-1]
 print(str(rsi))
 
 
 #-----------------------------------------------------------------------------------MACD indicator---------------------------------------------
 
 macd, macdsignal, macdhist = talib.MACD(Close_value, fastperiod=12, slowperiod=26, signalperiod=9)
 
 m=pd.DataFrame({'date':macd.index,'macd':macd.values})
 n=pd.DataFrame({'date':macdsignal.index,'macdsignal':macdsignal.values})
 o=pd.DataFrame({'date':macdhist.index,'macdhist':macdhist.values})
 MACD_value=m["macd"].iloc[-1]
 MACDSignal_value=n["macdsignal"].iloc[-1]
 MACDHist_value=o["macdhist"].iloc[-1]
 
 print("macd :" + str("%.2f" % MACD_value))
 print("macdsignal :" + str("%.2f" % MACDSignal_value))
 print("macdhist :" + str("%.2f" % MACDHist_value))
 
 
 # -----------------------------------------------------------------------------PSAR indicator---------------------------------------------

 psarHigh = sbin['High']
 psarLow = sbin['Low']
 psarClose = sbin['Close']
 parabolicsar = talib.SAR(psarHigh, psarLow, acceleration=0.02, maximum=0.2)[-1]
 print(SYMBOL + " psar is :" + str("%.2f" % parabolicsar))
 change = (parabolicsar - psarClose[-1]) / parabolicsar
 perChange = change * 100
 
 # if perChange is negative this implies that psar is some % below the closing price=>selling indicator
 # if perChange is positive this implies that psar is some % above the closing price=>buying indicator
 
 print (SYMBOL +" psar change :"+ str("%.2f" % perChange))

 # ------------------------------------------------------------------------------conditions --------------------------------------------------------------


 if (20 < rsi < 80) and (perChange == float(30)):
  MSG = 'Normal call for ' + SYMBOL + ' RSI is: ' + str("%.2f" % rsi) +'\r' + 'psar is : '+ str("%.2f" % parabolicsar)
  MsgNormalArray.append(MSG)
  print(MSG + " for Date " + str(Today))
 if  (rsi>=80 and float(0) < perChange <= float(30)):
  MSG = 'SELL call for ' + SYMBOL + ' RSI is: ' + str("%.2f" % rsi) +'\r' + 'psar is : '+ str("%.2f" % parabolicsar)
  MsgSellArray.append(MSG)
  print(MSG + " for Date " + str(Today))
 if (rsi <= 20) and (float(-30) < perChange < float(0)):
  MSG = 'BUY call for ' + SYMBOL + ' RSI is: ' + str("%.2f" % rsi) +'\r' + 'psar is : '+ str("%.2f" % parabolicsar)
  MsgBuyArray.append(MSG)
  print(MSG + " for Date " + str(Today))

MsgNormalArray = '\n'.join(MsgNormalArray)
MsgBuyArray = '\n'.join(MsgBuyArray)
MsgSellArray = '\n'.join(MsgSellArray)




messageNormal = """\
Subject :Normal NSE Report : From Rajat

"""+MsgNormalArray


messageSell = """\
Subject :Sell NSE Report : From Rajat

"""+MsgSellArray



messageBuy = """\
Subject :Buy NSE Report : From Rajat

"""+MsgBuyArray

li = ["myntrarajat26@gmail.com", "rajatjain2625@gmail.com"] 

if len(MsgNormalArray) != 0:
 for i in range(len(li)):
  s = smtplib.SMTP('smtp.gmail.com', 587)  
  s.starttls() 
  s.login("rajatjain2625@gmail.com", "**password**")  
  s.sendmail("rajatjain2625@gmail.com", li[i], messageNormal) 
  s.quit()
  print('mail sent !!')


if len(MsgBuyArray) != 0:
 for i in range(len(li)): 
  s = smtplib.SMTP('smtp.gmail.com', 587)  
  s.starttls() 
  s.login("rajatjain2625@gmail.com", "**password**")
  s.sendmail("rajatjain2625@gmail.com", li[i], messageBuy) 
  s.quit()
  print('mail sent !!')

if len(MsgSellArray) != 0:
 for i in range(len(li)): 
  s = smtplib.SMTP('smtp.gmail.com', 587)  
  s.starttls() 
  s.login("rajatjain2625@gmail.com", "**password**")
  s.sendmail("rajatjain2625@gmail.com", li[i], messageSell) 
  s.quit()
  print('mail sent !!')
