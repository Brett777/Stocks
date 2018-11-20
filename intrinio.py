import pandas as pd
import requests

username = 'f7f07a1366bd4e63b3ade2edcec06274'
password = 'ed7455b4da237cbdf878db9cd01df6f4'
base_url = "https://api.intrinio.com"

ticker = "MSFT"
request_url = base_url + "/financials/standardized"
query_params = {
    'ticker': ticker,
    'statement': 'income_statement',
    'fiscal_year': '2018',
    'fiscal_period' : 'Q1'
}


response = requests.get(request_url, params=query_params, auth=(username, password))
data = response.json()['data']

df = pd.DataFrame(data)
#df = df['data'].apply(pd.Series)
df = df.transpose()

print(data)
