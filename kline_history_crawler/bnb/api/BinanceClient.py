import json
import time

from binance.client import Client
from service.handler import ResultHandler


class BnbRestApiClient:
    def __init__(self):
        self.client = Client('AbEIrslVmOD7sSL4qwEUiuDIsD1DxG7LT9b5ODmMmZemvQotxDaRX1kGzgggwPUu',
                             'VLXzhtrihiC8nZnB4uZlj1qi3YqN4bGJKjJO8hv4ZULw54BGPPwNBjTPbnhuDg36')

    def trade_detail(self, symbol, interval):
        init_data = None
        handler = ResultHandler(3, symbol)
        while True:
            try:
                if init_data is None:
                    init_data = self.client.get_aggregate_trades(symbol=symbol.upper() + 'USDT', limit=1)[0]
                while True:
                    time.sleep(10)
                    result = self.client.get_aggregate_trades(symbol=symbol.upper() + 'USDT', fromId=init_data['a'])
                    init_data = result[-1]
                    handler.handle_result(result, interval)
            except Exception as e:
                print('币安请求接口异常：{}', e)
                pass


bnbRestClient = BnbRestApiClient()

