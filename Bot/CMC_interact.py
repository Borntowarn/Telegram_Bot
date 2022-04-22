from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class CMC_API:
    """This object represents a CoinMarketCap interaction."""
    
    token = '9273b9b2-6158-428f-afd4-379f3c3992de'
    url = 'https://pro-api.coinmarketcap.com'
    urls = {
      'map': f'{url}/v1/cryptocurrency/map',
      'latestData': f'{url}/v2/cryptocurrency/quotes/latest',   
      'fiat': f'{url}/v1/fiat/map'
      }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '9273b9b2-6158-428f-afd4-379f3c3992de',
    }


    def __init__(self) -> None:
        self.session = Session()
        self.session.headers.update(self.headers)
        
        try:
            response_fiat = self.session.get(self.urls['fiat'])
            response_crypto = self.session.get(self.urls['map'])
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return(e)
        
        self.ID_to_SYM = {}
        self.SYM_to_ID = {}
        ID = json.loads(response_fiat.text)['data']
        crypto_ID = json.loads(response_crypto.text)['data']
        ID.extend(crypto_ID)
        for item in ID:
            self.ID_to_SYM[item['id']] = item['symbol']
            if item['symbol'] in self.SYM_to_ID.keys():
                self.SYM_to_ID[item['symbol']] = [self.SYM_to_ID[item['symbol']]]
                self.SYM_to_ID[item['symbol']].append(item['id'])
            else: 
                self.SYM_to_ID[item['symbol']] = item['id']
            
            
        

    def get_price_change(self, symbols, period='1h', convert='USD'):
        """
        Method returns price changings for a setted period

        Args:
            symbols (:obj:`str`): Comma-separated list
                of symbols of cryptocurrencies to check.
            
            period (:obj:`str`, optional): Price changing period. Defaults to '1h'.
            
            convert (:obj:`str`, optional): Comma-separated list
                of symbols of crypto(currencies) for converting. Defaults to 'USD'.

        Returns:
            :obj:`map`: Map where keys are symbols of token 
                value is a map where
                link is a CMC token link
                price is a tuple of currency, current price and percent change for the period.

        """
        try:
            data = self.get_stat(symbols, convert)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return(e)

        prices = {}
        for key, item in data.items():
            prices[item['symbol']] = {
                'link': item['link'],
                'price': [
                    (
                    self.ID_to_SYM[int(quote)], 
                    price['price'], 
                    price[f'percent_change_{period}']
                    ) 
                    for quote, price in item['quote'].items()]
            }
        return prices
        
        

    def get_stat(self, symbols, convert='USD'):
        """
        Function returns all statistics for needed cryptocurrencies

        Args:
            symbols (:obj:`str`): Comma-separated list
                of symbols of cryptocurrencies to check.
            convert (:obj:`str`, optional): Comma-separated list
                of symbols of crypto(currencies) for conversion. Defaults to 'USD'.
        
        Returns:
            :obj:`map`: A map of cryptocurrency objects
                by ID, symbol, or slug (as used in query parameters)
        """
        try:
            ids = self.get_CMC_id(convert)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return(e)
        
        parameters = {
          'symbol': symbols,
          'convert_id': ids
        }
        
        data = {}
        response = self.session.get(self.urls['latestData'], params=parameters)
        for key, value in json.loads(response.text)['data'].items():
            data[key] = value[0]
        for key, value in data.items():
            data[key]['link'] = 'https://coinmarketcap.com/currencies/' + data[key]['slug']
        return data

    
    def get_CMC_id(self, symbols):
        """_summary_

        Args:
            symbols (:obj:`str`): Comma-separated list of symbols of cryptocurrencies to check.

        Returns:
            :obj:`str`: Comma-separated list of ids of cryptocurrencies to check.
            
        """
        
        symbols = [i.strip().upper() for i in symbols.split(',')]
        ids = [str(self.SYM_to_ID[i]) for i in symbols]
        return ','.join(ids)