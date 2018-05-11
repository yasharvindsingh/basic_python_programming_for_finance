import pandas as pd
import numpy as np
import xlrd
from fredapi import Fred



x1 = pd.ExcelFile("df.xlsx")

print(x1.sheet_names)

df = x1.parse('Crisis Years')
print('Description:')
print(df.describe())
print('Head:')
print(df.head())

fred = Fred(api_key='7811f9796f9d5963abc9f57d2f710511')
data = fred.get_series('SP500', observation_start='2000-01-01')

print(data.head())

data.to_csv('fred_sp500.csv')

https://finance.yahoo.com/quote/FRED/history?period1=950034600&period2=1518114600&interval=1d&filter=history&frequency=1d