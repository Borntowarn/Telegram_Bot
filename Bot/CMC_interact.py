"""
Взаимодействие с API сайта CoinMarketCap
"""

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


token = '9273b9b2-6158-428f-afd4-379f3c3992de'

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

parameters = {
  'start':'1',
  'limit':'2',
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '9273b9b2-6158-428f-afd4-379f3c3992de',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)