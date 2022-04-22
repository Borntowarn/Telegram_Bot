from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class CMC_API:
    token = '9273b9b2-6158-428f-afd4-379f3c3992de'
    url = 'https://pro-api.coinmarketcap.com'
    urls = {
      'map': f'{url}/v1/cryptocurrency/map',
      'latestData': f'{url}/v2/cryptocurrency/quotes/latest',
      'newListings': f'{url}/v1/cryptocurrency/listings/new',
      'airdrops': f'{url}/v1/cryptocurrency/airdrops',
      'fiat': f'{url}/v1/fiat/map'
      }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '9273b9b2-6158-428f-afd4-379f3c3992de',
    }


    def __init__(self) -> None:
        self.session = Session()
        self.session.headers.update(self.headers)


    def get_stat(self, symbols='', convert='USD'):
        parameters = {
          'symbol': symbols,
          'convert_id': self.get_CMC_id(convert)
        }
        try:
          response = self.session.get(self.urls['latestData'], params=parameters)
          data = json.loads(response.text)
          return(data['data'])
        except (ConnectionError, Timeout, TooManyRedirects) as e:
          return(e)
      
    
    def get_CMC_id(self, symbols):
        """
        Function helper

        Args:
            symbols (str): Comma-separated list of symbols of crypto(currencies)

        Returns:
            str: symbols (str): Comma-separated list of CMC_ID of crypto(currencies)
        """
        symbols = [i.strip().upper() for i in symbols.split(',')]
        try:
          response_fiat = self.session.get(self.urls['fiat'])
          response_crypto = self.session.get(self.urls['map'])
          data = json.loads(response_fiat.text)['data']
          crypto_data = json.loads(response_crypto.text)['data']
          
          data.extend(crypto_data)
          ids = [str(item['id']) for item in data if item['symbol'] in symbols]
          return ','.join(ids)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
          return(e)