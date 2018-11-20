from sqlalchemy import create_engine
import random
from indicators import *
from transform import *
import pandas_datareader as web
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
#import h2o
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF
#import cufflinks as cf
#from plots import *
import numpy as np
import operator
import math

stockSymbol = "PINC"
market = "NASDAQ"
invest = 1000

window = 15
start_date = pd.datetime(2013,1,1)
split_test = pd.datetime(2018,8,1)

df = web.DataReader(stockSymbol, 'iex', start=start_date)
df = df.reset_index(drop=False)
df.set_index('date', inplace=True)
df.columns = ['Open','High', 'Low', 'Close','Volume']
df.head(10)

df.reset_index(drop=False, inplace=True, col_level=0)


chaikin_oscillator(df, periods_short=3, periods_long=10, high_col='High', low_col='Low', close_col='Close', vol_col='Volume')
acc_dist(df, trend_periods=21, open_col='Open', high_col='High', low_col='Low', close_col='Close', vol_col='Volume')
price_volume_trend(df, trend_periods=21, close_col='Close', vol_col='Volume')
average_true_range(df, trend_periods=14, open_col='Open', high_col='High', low_col='Low', close_col='Close', drop_tr=True)
typical_price(df, high_col = 'High', low_col = 'Low', close_col = 'Close')
money_flow_index(df, vol_col='Volume')
rsi(df, close_col='Close')
ema(df, period=26, column='Close')
ema(df, period=12, column='Close')
macd(df, period_long=26, period_short=12, period_signal=9, column='Close')
on_balance_volume(df, trend_periods=21, close_col='Close', vol_col='Volume')
price_volume_trend(df, trend_periods=21, close_col='Close', vol_col='Volume')
bollinger_bands(df, trend_periods=20, close_col='Close')
williams_r(df, periods=14, high_col='High', low_col='Low', close_col='Close')
ultimate_oscillator(df, period_1=7,period_2=14, period_3=28, high_col='High', low_col='Low', close_col='Close')
df = df.drop(['uo_bp', 'uo_tr', 'uo_avg_1', 'uo_avg_2', 'uo_avg_3'], axis=1)
df.rename(columns={'date': 'Date'}, inplace=True)
df['Date'] =  pd.to_datetime(df['Date'])

df = df.drop(df.index[0:27])
df.reset_index(drop=False, inplace=True, col_level=0)

# Tomorrow's Close. This is the target column
df['Close Tomorrow'] = df['Close'].shift(-1)
df['Close Tomorrow Change'] = df['Close Tomorrow'] - df['Close']
df['Close Tomorrow Trend'] = df['Close Tomorrow Change'].apply(np.sign)
df['Close Tomorrow Trend'].replace(0,-1,inplace=True)

df = df.drop(['Close Tomorrow','Close Tomorrow Change'], axis=1)
df.drop(df.tail(1).index,inplace=True)
df.head()

trainingDF = df.loc[df['Date'] <= split_test]
testDF = df.loc[df['Date'] > split_test]

trainingDF.to_csv("PINCStockTrend-train.csv")
testDF.to_csv("PINCStockTrend-test.csv")