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

server ='api-fxpractice.oanda.com'
#granularity = 'H1'
#instrument = 'GBP_JPY'

now_date = datetime.date.today()
now_time = datetime.datetime.now()
cur_hour = now_time.hour # Час текущий
cur_minute = now_time.minute # Минута текущая

#start_hour = cur_hour - 1

#d = [1,2,3,4,5,7,2,3,4,1,2,6,5,3,4,6]
#m = []

is_dst = time.daylight and time.localtime().tm_isdst > 0
utc_offset = (time.altzone if is_dst else time.timezone)
def getGranularitySeconds(granularity):
    if granularity[0] == 'S':
        return int(granularity[1:])
    elif granularity[0] == 'M' and len(granularity) > 1:
        return 60*int(granularity[1:])
    elif granularity[0] == 'H':
        return 60*60*int(granularity[1:])
    elif granularity[0] == 'D':
        return 60*60*24
    elif granularity[0] == 'W':
        return 60*60*24*7
    #Does not take into account actual month length
    elif granularity[0] == 'M':
        return 60*60*24*30

#Надо сделать, чтоб постоянно запрашивал closeMid
def connection():
 global candle
 headers = {'Authorization' : 'Bearer ' + "c1d60b84697cdc6e0c26684a42e54190-13a1e440394be03e6723bc09b4b75955"}
 s = requests.Session()
 r = s.get('https://api-fxpractice.oanda.com/v1/accounts', headers=headers, verify=True)
 r = s.get('https://' + server + '/v1/candles?instrument=' + instrument + '&count=2&candleFormat=midpoint&granularity='+ granularity + '&dailyAlignment=0&alignmentTimezone=America%2FNew_York', headers=headers)
 candle = r.text
 #return candle
connection()

def strip_candel():
 global closeMid_first, closeMid_second

 msg = json.loads(candle)
 data = json.dumps(msg)
 closeMid_first = data[69:77] #191.6275
 closeMid_second = data[226:233] #191.7545 - меняется. надо понять что это
 m.insert(+1, str(closeMid_first))  
 return closeMid_first
 return m
 #print data

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
print SMA(d, 4)
#EMA 80 + 200
print EMA(d, 2)
strip_candel()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Give me a candle size (1H, 15M) and pair (GBP_JPY, EUR_USD)!"
        sys.exit()
    else:
        granularity, instrument = sys.argv[1:]
        compareAndTrade(granularity, instrument)