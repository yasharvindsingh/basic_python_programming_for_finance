import bs4 as bs
import datetime as dt 
import os 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd 
import pandas_datareader.data as web
import pickle
import requests

style.use('ggplot')

def save_sp500_tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	# headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
	# resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',headers = headers)
	if resp == None:
		print('resp : None')
	soup = bs.BeautifulSoup(resp.text, 'lxml')
	if soup == None:
		print('soup : None')
	table = soup.find('table',{'class':'wikitable sortable'})
	if table == None:
		print('table : None')
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker)

	with open('sp500tickers.pickle',"wb") as f:
		pickle.dump(tickers,f)

	print(tickers)

	return tickers

# save_sp500_tickers()

def present_tickers(have,not_have):
	for i in not_have:
		have.remove(i)
	with open('present_tickers.pickle',"wb") as f:
		pickle.dump(have,f)


def get_data_from_web(reload_sp500 = False):
	tickers=None
	if reload_sp500:
		tickers = save_sp500_tickers()
	else:
		with open('sp500tickers.pickle',"rb") as f:
			tickers = pickle.load(f)

	if not os.path.exists('stock_dfs'):
		os.makedirs("stock_dfs")

	start = dt.datetime(2000, 1, 1)
	end = dt.datetime(2016, 12, 31)
	not_found=[]
	for ticker in tickers:
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			print(ticker)
			try:
				df = web.DataReader(ticker,'morningstar',start,end) # 'google' 'morningstar' 'stooq' 
				df.to_csv('stock_dfs/{}.csv'.format(ticker))
				print(ticker)
			except:
				not_found.append(ticker)
				print('did not find {} on google'.format(ticker))

		else:
			print('Already have {}'.format(ticker))

	print(not_found)
	# if len(not_found) > 0:
	present_tickers(tickers, not_found)
	


# get_data_from_web()

def compile_data():
	with open('sp500tickers.pickle','rb') as f:
		tickers=pickle.load(f)
	main_df = pd.DataFrame()
	not_good_col=[]
	for count,ticker in enumerate(tickers):
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		print(ticker,df.columns)
		df.set_index('Date', inplace=True)
		df.rename(columns = {'Close': ticker}, inplace = True)
		try:
			df.drop(["Open","High","Low","Volume"], axis=1, inplace = True)

			if main_df.empty:
				main_df =df
			else:
				main_df = main_df.join(df ,how ='outer')
		except:
			not_good_col.append(ticker)
			print('Did not find a col')
		if count % 10 == 0:
			print(count)
	print(len(not_good_col))
	print(main_df.head())
	null_columns=main_df.columns[main_df.isnull().any()]
	print(null_columns)
	# main_df[null_columns].isnull().sum()

	main_df.to_csv("sp500_joined_close.csv")

compile_data()

def visualize_data():
	df = pd.read_csv("sp500_joined_close.csv")
	# df['AAPL'].plot()
	# plt.show()
	df_corr = df.corr()
	print(df_corr.head())

	data = df_corr.values
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)

	heatmap = ax.pcolor(data,cmap=plt.cm.RdYlGn)
	fig.colorbar(heatmap)
	ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	column_labels = df_corr.columns
	row_labels = df_corr.index

	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_labels)
	plt.xticks(rotation=90)
	heatmap.set_clim(-1,1)
	plt.tight_layout()
	plt.show()

# visualize_data()