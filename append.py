import os 
import pandas as pd 
import pickle

with open('present_tickers.pickle',"rb") as f:
	tickers = pickle.load(f)
print(tickers)
for ticker in tickers:
	df = pd.read_csv('stock_dfs/{}.csv'.format(ticker), index_col=False)
	if ticker == 'NBL':
		print(df.columns)
	if 'Symbol' in df.columns:
		print(ticker)
		df = df[['Date','Open','High','Close','Volume']]
		df.to_csv('stock_dfs/{}.csv'.format(ticker),header = ['Date','Open','High','Close','Volume'],index = False)