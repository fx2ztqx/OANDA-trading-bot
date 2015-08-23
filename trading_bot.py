#!/usr/bin/python
# -*- coding: UTF-8 -*-

#ACCESS TOKEN
#c1d60b84697cdc6e0c26684a42e54190-13a1e440394be03e6723bc09b4b75955
#ID_CLIENT
#2227972


import requests
import re
import json
import datetime
import sys
import numpy as np
import time
import datetime


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Give me a candle size [1H, 15M], instrument [GBP_JPY, EUR_USD], SMA period [80, 200] and EMA period [80,200]!"
        sys.exit()
    else:
        granularity = sys.argv[1]
        instrument = sys.argv[2]
        sma_period= int(sys.argv[3])
        ema_period = int(sys.argv[4])

server ='api-fxpractice.oanda.com'
#granularity = 'H1'
#instrument = 'GBP_JPY'

now_date = datetime.date.today()
now_time = datetime.datetime.now()
cur_hour = now_time.hour # Час текущий
cur_minute = now_time.minute # Минута текущая


d = [1,2,3,4,5,7,2,3,4,1,2,6,5,3,4,6]
#m = []


def connection():
 global candle
 headers = {'Authorization' : 'Bearer ' + "c1d60b84697cdc6e0c26684a42e54190-13a1e440394be03e6723bc09b4b75955"}
 s = requests.Session()
 r = s.get('https://api-fxpractice.oanda.com/v1/accounts', headers=headers, verify=True)
 r = s.get('https://' + server + '/v1/candles?instrument=' + instrument + '&count=2&candleFormat=midpoint&granularity='+ granularity + '&dailyAlignment=0&alignmentTimezone=America%2FNew_York', headers=headers)
 candle = r.text
 #return candle
connection()


#Have to fix
def strip_candel():
 global closeMid_first, closeMid_second

 msg = json.loads(candle)
 data = json.dumps(msg)
 closeMid_first = data[69:77] 
 closeMid_second = data[226:233] 
 #m.insert(+1, str(closeMid_first))  
 return closeMid_first
 #return m


print strip_candel()

def SMA(values, window):
 weights = np.repeat(1.0, window)/window
 smas = np.convolve(values, weights, 'valid')

 return smas

def EMA(values, window):
 weights = np.exp(np.linspace(-1.,0.,window))
 weights /= weights.sum()
 
 a = np.convolve(values, weights) [:len(values)]
 a[:window] = a[window]
 return a 

#SMA 80 + 200
print SMA(d, sma_period)
#EMA 80 + 200
print EMA(d, ema_period)
strip_candel()

