import pandas as pd
from pandas.io.json import json_normalize
import requests


key = '6b57487789d6f79fe484f7a043be8f90:51fcb919d122fdaa2e7bb1cf9d2d680b'


stock = "MSFT"
base_url = "https://api.gurufocus.com/public/user/"


response = requests.get(base_url + key + "/stock/" + stock + "/financials")
data = response.json()
df = pd.read_json(data, typ='series', orient='columns')





df = pd.io.json.json_normalize(data, '')
#df.columns = df.columns.map(lambda x: x.split(".")[-1])

print(df.shape)


print(df)