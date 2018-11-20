import pandas as pd
import iexfinance as iex
from datetime import datetime


start = datetime(2017, 2, 9)
end = datetime(2017, 5, 24)

msft = iex.Stock("MSFT", output_format='json')
msftEarnings = msft.get_earnings()
msftFinance = msft.get_financials()



dfEarn = pd.DataFrame(msftEarnings)
dfFin = pd.DataFrame(msftFinance)

df = iex.get_historical_data("MSFT", start, end, output_format="pandas")
df

test = iex.StockReader.get_earnings. get_market_book("msft", output_format="json")