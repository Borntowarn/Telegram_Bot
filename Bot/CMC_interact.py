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
        
        self.ID_to_SYM = {} #Таблица соответствия CMC id и символа
        self.SYM_to_ID = {} #Таблица соответствия символа и CMC id
        ID = json.loads(response_fiat.text)['data']
        crypto_ID = json.loads(response_crypto.text)['data']
        ID.extend(crypto_ID)
        for item in ID:
            self.ID_to_SYM[item['id']] = item['symbol']
            if item['symbol'] in self.SYM_to_ID.keys():
                if isinstance(self.SYM_to_ID[item['symbol']], int):
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
            
            period (:obj:`str`, optional): Comma-separated list
                of periods of periods to check. Can be '1h', '24h', '7d', '30d'.
                Defaults to '1h'.
            
            convert (:obj:`str`, optional): Comma-separated list
                of symbols of crypto(currencies) for converting. Defaults to 'USD'.

        Returns:
            :obj:`map`: A map where:
                :obj:`keys`: Symbols of token.
                
                :obj:`values`: Maps where:
                
                    :obj:`link`: A CMC token link.
                
                    :obj:`price`: A map where:
                    
                        :obj:`keys`: Symbols of crypto(currency).
                
                        :obj:`values`: Maps where:
                
                            :obj:`price`: Current price.
                
                            :obj:`changes`: A map where:
                            
                                :obj:`keys`: Period.
                
                                :obj:`values`: Changes.

        """
        try:
            data = self.get_stat(symbols, convert)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return(e)

        periods = [i.strip() for i in period.split(',')]
        prices = {}
        for key, item in data.items():
            prices[item['symbol']] = {
                'link': item['link'],
                'price': {
                    quote:
                        {
                        'price': price['price'], 
                        'changes': {period: price[f'percent_change_{period}'] for period in periods}
                        }
                    for quote, price in item['quote'].items()
                }
            }
        return prices
    
    
    def get_market_pairs(self, symbols):
        """
        Method returns CMC number of market pairs for setted cryptocurrencies

        Args:
            symbols (:obj:`str`): Comma-separated list
                of symbols of cryptocurrencies to check.

        Returns:
            :obj:`map`: A map where:
            
                :obj:`keys`: Symbols of token.
                
                :obj:`values`: Maps where:
                
                    :obj:`link`: A CMC token link.
                
                    :obj:`pairs`: Number of pairs.

        """
        try:
            data = self.get_stat(symbols)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return(e)
        
        pairs = {}
        for key, item in data.items():
            pairs[item['symbol']] = {
                'link': item['link'],
                'pairs': item['num_market_pairs']
            }
        return pairs
        
     
    def get_CMC_rank(self, symbols):
        """
        Method returns CMC ranks for setted cryptocurrencies

        Args:
            symbols (:obj:`str`): Comma-separated list
                of symbols of cryptocurrencies to check.

        Returns:
            :obj:`map`: A map where:
            
                :obj:`keys`: Symbols of token.
                
                :obj:`values`: Maps where:
                
                    :obj:`link`: A CMC token link.
                
                    :obj:`rank`: Rank.

        """
        try:
            data = self.get_stat(symbols)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return(e)
        
        ranks = {}
        for key, item in data.items():
            ranks[item['symbol']] = {
                'link': item['link'],
                'rank': item['cmc_rank']
            }
        return ranks
       
    
    def get_volume(self, symbols):
        """
        Method returns value and changings for a setted period

        Args:
            symbols (:obj:`str`): Comma-separated list
                of symbols of cryptocurrencies to check.

        Returns:
            :obj:`map`: A map where:
            
                :obj:`keys`: Symbols of token.
                
                :obj:`values`: Maps where:
                
                    :obj:`link`: A CMC token link.
                
                    :obj:`volume`: Trading volume.
                    
                    :obj:`changes`: Volume changes for 24h.
        """
        
        try:
            data = self.get_stat(symbols)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return(e)
        
        volumes = {}
        for key, item in data.items():
            volumes[item['symbol']] = {
                'link': item['link'],
                'volume': item['quote']['USD']['volume_24h'], 
                'changes': item['quote']['USD']['volume_change_24h']
            }
        return volumes
        
        
    def get_stat(self, symbols, convert='USD'):
        """
        Function returns full statistics for needed cryptocurrencies

        Args:
            symbols (:obj:`str`): Comma-separated list
                of symbols of cryptocurrencies to check.
            convert (:obj:`str`, optional): Comma-separated list
                of symbols of crypto(currencies) for conversion. Defaults to 'USD'.
        
        Returns:
            :obj:`map`: A map of full stat of cryptocurrency objects by symbol.
                Keys for map you can look `here <https://coinmarketcap.com/api/documentation/v1/#operation/getV2CryptocurrencyQuotesLatest>`_
        """
        
        #Получение CMC id для валют конвертации
        # try:
        #     ids = self.get_CMC_id(convert)
        # except (ConnectionError, Timeout, TooManyRedirects) as e:
        #     return(e)
        
        #Разделяем параметры конвертации для того, чтобы запросы проходили обработку
        #так как наш план API поддерживает только одну валюту для конвертации
        parameters = [{
          'symbol': symbols.replace(' ', ''),
          'convert': i.strip()
        } for i in convert.split(',')]
        
        
        #Отправляем по запросу на каждую валюту конвертации и после
        #этого объединяем запросы в один со всеми валютами конвертации
        responses = []
        for parameter in parameters:
            response = self.session.get(self.urls['latestData'], params=parameter)
            responses.append(json.loads(response.text)['data'])
        for key, value in responses[0].items():
            responses[0][key] = value[0]
        for response in responses[1:]:
            for key, item in response.items():
                responses[0][key]['quote'].update(item[0]['quote'])
        data = responses[0]
        
        #Добавление ссылок на страницу валюты в CMC
        for key, value in data.items():
            data[key]['link'] = 'https://coinmarketcap.com/currencies/' + data[key]['slug']
        return data

    
    def get_CMC_id(self, symbols):
        """
        Method returns CMC's ids for symbols of currencies

        Args:
            symbols (:obj:`str`): Comma-separated list of symbols of cryptocurrencies to check.

        Returns:
            :obj:`str`: Comma-separated list of ids of cryptocurrencies to check.
            
        """
        
        symbols = [i.strip().upper() for i in symbols.split(',')]
        ids = [str(self.SYM_to_ID[i]) for i in symbols]
        return ','.join(ids)
