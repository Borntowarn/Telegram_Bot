from Bot.CMC_interact import CMC_API

cl = CMC_API()

def test_get_CMC_id():
    assert cl.get_CMC_id(symbols='btc') == '1'