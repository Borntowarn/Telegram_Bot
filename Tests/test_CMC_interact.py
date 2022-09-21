from Bot.CMC_interact import CMC_API
import unittest

class TestCMC(unittest.TestCase):
    def setUp(self):
        self.cmc = CMC_API()

    def test_getprice_1h(self):
        self.assertEqual(self.cmc.get_price_change('ETH', '1h')['ETH']['name'], 'Ethereum')


    def test_getprice_24h(self):
        self.assertEqual(self.cmc.get_price_change('Eth', '24h')['ETH']['name'], 'Ethereum')
    

    def test_getvolume(self):
        self.assertEqual(self.cmc.get_volume('ETH')['ETH']['link'], 'https://coinmarketcap.com/currencies/ethereum')


    def test_getprice_EU(self):
        self.assertEqual(self.cmc.get_price_change('Eth', '30d', 'EU'), {'ETH': {'link': 'https://coinmarketcap.com/currencies/ethereum', 'name': 'Ethereum', 'price': {{'price': 1349.2915199204488, 'changes': {'30d': -1.24466457}}}}})


if __name__ == "__main__":
    unittest.main()