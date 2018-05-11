import os 
import pandas as pd 
import pickle
with open('sp500tickers.pickle',"rb") as f:
	tickers = pickle.load(f)
c=0
count=0
for ticker in tickers:
	c=0
	try:
		with open('stock_dfs/{}.csv'.format(ticker)) as f:
			lines = f.readlines()
			if 'No data' in lines[0]:
				c=1
		if c==1:
			os.remove('stock_dfs/{}.csv'.format(ticker))
			count+=1
	except:
		print('File {} not there..'.format(ticker))
print('count deleted: ',count)