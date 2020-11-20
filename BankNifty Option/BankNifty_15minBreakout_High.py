# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import smtplib,ssl
import math
import pandas as pd
import time  as _time
import numpy
from datetime import datetime, timedelta
import requests

from twilio.rest import Client
from twilio.rest import Client 


account_sid = '****' 
auth_token = '****' 
client = Client(account_sid, auth_token) 



stock_Symbol="^NSEBANK"
#stock_Symbol="VEDL.NS"

##================================== Alert for 15 min Higher breakout level =========================================


class YahooFinance:
    def start(self, ticker, result_range='1mo', start=None, end=None, interval='15m', dropna=True):
       
        # "1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max
        # Valid Intervals - Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
        if result_range is None:
            start = int(_time.mktime(_time.strptime(start, '%d-%m-%Y')))
            end = int(_time.mktime(_time.strptime(end, '%d-%m-%Y')))
            # defining a params dict for the parameters to be sent to the API
            params = {'period1': start, 'period2': end, 'interval': interval}
        else:
            params = {'range': result_range, 'interval': interval}
        # sending get request and saving the response as response object
        url = "https://query1.finance.yahoo.com/v8/finance/chart/{}".format(ticker)
        r = requests.get(url=url, params=params)
        data = r.json()
        # Getting data from json
        error = data['chart']['error']
        if error:
            raise ValueError(error['description'])
        self._result = self._parsing_json(data)
        if dropna:
            self._result.dropna(inplace=True)
        return self._result


    def get_Live_data():
      #while(1==1):
      page=requests.get('https://in.finance.yahoo.com/quote/'+stock_Symbol+'?p='+stock_Symbol+'&.tsrc=fin-srch')
      soup=BeautifulSoup(page.text,'lxml')
      dataArray=soup.find_all('div',{'class':"My(6px) Pos(r) smartphone_Mt(6px)"})[0].find('span').text
      print(dataArray)

    def send_WhatsApp(self,msg):
      message = client.messages.create( 
                              from_='whatsapp:****',  
                              body="🤑Alert🔔from✅⚡⚡Rajat⚡⚡✅\n"+msg,      
                              to='whatsapp: enter mobile here'
                          )
      print("sms sent !!")      


    def send_Mail(self , msg):
      messageBuy = """\
Subject :NSE Report : From Rajat

"""+msg

      li = ["recepientEmail@gmail.com","recepientEmail@gmail.com"] 

      if len(messageBuy) != 0:
        for i in range(len(li)):
          s = smtplib.SMTP('smtp.gmail.com', 587)  
          s.starttls() 
          s.login("youremail@gmail.com", "**password**")  
          s.sendmail("youremail@gmail.com", li[i], messageBuy) 
          s.quit()
          print('mail sent !!')


    def _parsing_json(self, data):
        timestamps = data['chart']['result'][0]['timestamp']
        #print(timestamps)
        # Formatting date from epoch to local time
        timestamps = [_time.strftime('%a, %d %b %Y %H:%M:%S', _time.localtime(x)) for x in timestamps]
        #print(timestamps)
        volumes = data['chart']['result'][0]['indicators']['quote'][0]['volume']
        opens = data['chart']['result'][0]['indicators']['quote'][0]['open']
        opens = self._round_of_list(opens)
        closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
        closes = self._round_of_list(closes)
        lows = data['chart']['result'][0]['indicators']['quote'][0]['low']
        lows = self._round_of_list(lows)
        highs = data['chart']['result'][0]['indicators']['quote'][0]['high']
        highs = self._round_of_list(highs)
        df_dict = {'Open': opens, 'High': highs, 'Low': lows, 'Close': closes, 'Volume': volumes}
        df = pd.DataFrame(df_dict, index=timestamps)
        df.index = pd.to_datetime(df.index)
       # print(df.index+timedelta(hours = 5.5))
        return df

    def _round_of_list(self, xlist):
        temp_list = []
        for x in xlist:
            if isinstance(x, float):
                temp_list.append(round(x, 2))
            else:
                temp_list.append(pd.np.nan)
        return temp_list

    def to_csv(self, file_name):
        self.result.to_csv(file_name)

obj=YahooFinance()
res = obj.start(stock_Symbol, result_range='1d', interval='15m', dropna='True')
print(res.head())
#obj.send_Mail()

high_till_9_30=0;
Low_till_9_30=0;
risk_Margin=5;
prev_wk_low=0;
prev_wk_high=0;


for ind in res.index:  
  time = ind.strftime("%H:%M:%S")
  if time=="09:15:00":
    high_till_9_30=res['High'][ind]
    Low_till_9_30=res['Low'][ind]

print("till 9:30 low  --> " +str(Low_till_9_30))
print("till 9:30 High --> " +str(high_till_9_30))
print('\n')


res_5min = obj.start(stock_Symbol, result_range='1d', interval='5m', dropna='True')
count=0;
visited=[]
visited_alert=[]
msg_sent=False

resTest = obj.start(stock_Symbol,result_range='1mo', interval='1wk', dropna='True')
prev_week=resTest.iloc[[3]]
prev_wk_high=prev_week['High'][0]
prev_wk_low=prev_week['Low'][0]
print(resTest.iloc[[3]])


res__prev_1day = obj.start(stock_Symbol, result_range='5d', interval='1d', dropna='True')
print(res__prev_1day.iloc[[3]])
prev_day=res__prev_1day.iloc[[3]]
prev_day_high=prev_day['High'][0]
prev_day_low=prev_day['Low'][0]



while True :
  for indx in res_5min.index:
    time = indx.strftime("%H:%M:%S")
    if int (time.replace(':','')) >= 93000 and time not in visited :
      if "00" in time :
        message=""
        print("scanning for time --> " +time)
        # count=count+1
        # print(count)
        visited.append(time)
        local_high=res_5min['High'][indx]
        if  int(local_high) >= int(high_till_9_30 + risk_Margin) and time not in visited_alert :
          visited_alert.append(time)
          option_alert=int(math.floor(int(local_high) / 100.0)) * 100
          #print("option Alert ! Buy :" +"BANKNIFTY"+str(option_alert)+ "CE")
          option_alert_msg="\noption Alert ! Buy : ---> " +"BANKNIFTY"+str(option_alert)+ "CE"
          message="\n==============================="+option_alert_msg+"\n\nFor stock : "+stock_Symbol+"\n\nHigher than 9:30 high ie. " +str(high_till_9_30)+" ----> strike price  : "+str(local_high)+ " at time : "+ str(time) +"\n\n==============================="+"\n\nPrevious week high --> "+ str(prev_wk_high) +"\n\nPrevious week low --> "+ str(prev_wk_low)+"\n\n==============================="+"\n\nPrevious Day high --> "+str(prev_day_high)+"\n\nPrevious Day Low --> "+str(prev_day_low)+"\n\n==============================="
          print(message)
          #obj.send_Mail(message)
          obj.send_WhatsApp(message)
          msg_sent=True
          break
  if msg_sent!=True :
    print("sleep ")    
    _time.sleep(30)
    res_5min = obj.start(stock_Symbol, result_range='1d', interval='5m', dropna='True')
  else:
    break  
