#imports
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
import json

def lookup_fn(df, key_row, key_col):
    try:
        return df.iloc[key_row][key_col]
    except IndexError:
        return 0
    
    
def lookup_stockinfo(thestock):
  try:
    return thestock.info
  except IndexError:
    return 0

url = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
df=pd.read_csv(url, sep='|')
movementlist = []

#remove HEad for full listing
for stock in df['Symbol'].head(1): 
  # get history
  thestock = yf.Ticker(stock)
  hist = thestock.history(period="5d")
  # print(stock)
  low = float(10000)
  high = float(0)
  # print(thestock.info)
  for day in hist.itertuples(index=True, name='Pandas'):
    if day.Low < low:
      low = day.Low
    if high < day.High:
      high = day.High
  
  deltapercent = 100 * (high - low)/low
  Open = lookup_fn(hist, 0, "Open")
  # some error handling: 
  if len(hist >=5):
    Close = lookup_fn(hist, 4, "Close")
  else :
    Close = Open
  if(Open == 0):
    deltaprice = 0
  else:
    deltaprice = 100 * (Close - Open) / Open
  pair = [stock, deltapercent, deltaprice]
  movementlist.append(pair)


for entry in movementlist:
#  if entry[1]>float(100):
  #  print(entry)
    a = lookup_stockinfo(yf.Ticker(str(entry[0])))
    if a == 0:
            print("no info")
    else:
        if a is None:
            print("no info")
        else:
            if a == "":
                print("no")
            else:
               # print(a)
                print(json.dumps(a))


