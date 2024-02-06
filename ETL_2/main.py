import pandas as pd
import requests, json

url = "http://api.exchangeratesapi.io/v1/latest?base=EUR&access_key=5276e44e5844072db91a3026f66d9271"  #Make sure to change ******* to your API key.

res = requests.get(url)
res = json.loads(res.text)
df = pd.DataFrame(res, columns = ['rates'])
df.to_csv('rates.csv')