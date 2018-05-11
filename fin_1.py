import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas_datareader.data as web
import urllib

style.use('ggplot')

##start = dt.datetime(2000,1,1)
##end = dt.datetime(2016,12,31)
##
##df = web.get_data_google('TSLA', 
##                          start=start, 
##                          end=end)
# df=pd.read_csv('TSLA.csv', parse_dates = True, index_col=0)
##print(df.head())

##stock_price_url = 'https://pythonprogramming.net/yahoo_finance_replacement'
##source_code = urllib.request.urlopen(stock_price_url).read().decode()
##stock_data = []
##split_source = source_code.split('\n')
##
##columns = split_source.pop(0).split(',')
##print(columns)
##sp = list()
##for i in split_source:
##    sp.append(i.split(','))
##df = pd.DataFrame(np.array(sp))
##df.to_csv('tsla.csv',header = columns,index = False)

df=pd.read_csv('tsla.csv', parse_dates = True, index_col =0)

# print(df.head())
# df[].plot()
# plt.show()

# df['100ma'] = df['Adjusted_close'].rolling(window=100,min_periods=0).mean()
# print(df.head())

df_ohlc = df['Adjusted_close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

# print('df_ohlc')
# print(df_ohlc.head())


# print('df_volume')
# print(df_volume.head())

df_ohlc.reset_index(inplace = True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
# print(df_ohlc.head())

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex = ax1)

ax1.plot(df.index,df['Adjusted_close'])
# ax1.plot(df.index,df['100ma'])
ax2.bar(df.index,df['Volume'])
ax1.xaxis_date()

candlestick_ohlc(ax1,df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values,0)
plt.show()