import json
import pandas as pd
from pandas.io.json import json_normalize
import requests


#Set API key
key = '6b57487789d6f79fe484f7a043be8f90:51fcb919d122fdaa2e7bb1cf9d2d680b'

#Set Stock Symbol
stock = "MSFT"
base_url = "https://api.gurufocus.com/public/user/"

#Get fincial & fundamental data, filter for quarterly
response = requests.get(base_url + key + "/stock/" + stock + "/financials")
data = response.json()
df = pd.DataFrame.from_dict(data, orient="index")
df = df.loc[:,'quarterly']

#######################################
#  Reshape data for machine learning  #
#######################################

df = json_normalize(df).unstack().apply(pd.Series)
df = df.reset_index(drop=False)
df = df.drop('level_1', axis=1)
df = df.transpose()
df = df.reset_index(drop=True)
df.columns = df.iloc[0]
df = df.drop(0, axis=0)
df = df.reset_index(drop=True)
df['Fiscal Year'] = pd.to_datetime(df['Fiscal Year'])
df['Year'] = df['Fiscal Year'].dt.year
df['Month'] = df['Fiscal Year'].dt.month
df['Quarter'] = df['Year'].map(str) + "-" + df['Month'].map(str) #Will use this as a join key for merging stock prices

#################################
#  Get Historical Stock Prices  #
#################################

response2 = requests.get(base_url + key + "/stock/" + stock + "/price")
data2 = response2.json()
df2 = pd.DataFrame.from_dict(data2)
df2.columns = ['date','price']
df2 = df2.reset_index(drop=False)
df2['date'] = pd.to_datetime(df2['date'])
df2.set_index('date', inplace=True)
df2 = df2.groupby(pd.TimeGrouper(freq='Q')).mean()
df2['Year'] = df2.index.year
df2['Month'] = df2.index.month
df2['Quarter'] = df2['Year'].map(str) + "-" + df2['Month'].map(str)

# Join quarterly average price with quarterly financial data
df3 = pd.merge(df, df2[['price','Quarter']], on='Quarter')

# Shift quarterly average price back 1 period such that quarterly financials align with the NEXT quarter's price
df4 = df3
df4.price = df4.price.shift(-1)
df4 = df4.iloc[:-1]
df4.to_csv("ShiftTest.csv")

df4
