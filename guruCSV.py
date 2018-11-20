import pandas as pd
import pandas_datareader as web

dfFinancials = pd.read_csv("NAS_MSFT.csv")
dfFinancials = dfFinancials.transpose()

stockSymbol = "MSFT"
start_date = pd.datetime(2013,1,1)

df = web.DataReader(stockSymbol, 'iex', start=start_date)
df = df.reset_index(drop=False)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df.columns = ['Open','High', 'Low', 'Close','Volume']
df.head(10)



df = df.groupby(pd.TimeGrouper(freq='Q')).mean()