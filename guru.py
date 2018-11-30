import json
import pandas as pd
from pandas.io.json import json_normalize
import requests



key = '6b57487789d6f79fe484f7a043be8f90:51fcb919d122fdaa2e7bb1cf9d2d680b'


stock = "MSFT"
base_url = "https://api.gurufocus.com/public/user/"


response = requests.get(base_url + key + "/stock/" + stock + "/financials")
data = response.json()
df = pd.DataFrame.from_dict(data, orient="index")



df2 = json_normalize(data).apply(pd.Series).stack().reset_index()
df2[0] = df2[0].apply(pd.Series, index=df2.iloc[0,2])
