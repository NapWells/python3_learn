import json
import logging
import sys
import time
import requests

from service.handler import ResultHandler

log = logging.getLogger(__name__)
fh = logging.FileHandler('test.log')
fh.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
log.addHandler(sh)
log.addHandler(fh)
logging.basicConfig(level=logging.DEBUG, handlers=[fh, sh])


class BitfinexClient:

    def __init__(self):
        self.url = "https://api.bitfinex.com/v1/trades/%susd"

    def trade_detail(self, symbol, interval):
        init_data = None
        handler = ResultHandler(4, symbol)
        while True:
            try:
                if init_data is None:
                    init_response = requests.request("GET", self.url % symbol + '?limit_trades=1')
                    init_data = json.loads(init_response.text)[0]
                while True:
                    time.sleep(10)
                    response_result = requests.request("GET",
                                                       self.url % symbol + '?timestamp=%d' % (init_data['timestamp']))
                    result = json.loads(response_result.text)
                    result.sort(key=lambda k: (k.get('timestamp', 0)))
                    init_data = result[-1]
                    del(result[0])
                    handler.handle_result(result, interval)
            except Exception as e:
                logging.error('bitfinex请求接口异常：{}', e)
                pass


bitfinexClient = BitfinexClient()
if __name__ == '__main__':
    data = [{
        "timestamp": 1546582479,
        "tid": 329957453,
        "price": "3936.0",
        "amount": "0.76278597",
        "exchange": "bitfinex",
        "type": "buy"
    }, {
        "timestamp": 1546582476,
        "tid": 329957450,
        "price": "3936.0",
        "amount": "0.58345983",
        "exchange": "bitfinex",
        "type": "buy"
    }, {
        "timestamp": 1546582478,
        "tid": 329957449,
        "price": "3935.6",
        "amount": "0.039984",
        "exchange": "bitfinex",
        "type": "buy"
    }]
    data.sort(key=lambda k: (k.get('timestamp', 0)))
    # data = [i for i in data if i['timestamp'] >= 1546582478]
    # print(data)

    url = "https://api.bitfinex.com/v1/trades/btcusd?timestamp=1546849558"
    url = "https://api.bitfinex.com/v1/trades/btcusd?limit_trades=1"
    response = requests.request("GET", url)
    print(response.text)
