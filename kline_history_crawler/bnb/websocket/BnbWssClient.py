import json

from binance.client import Client
from service.handler import ResultHandler
from binance.websockets import BinanceSocketManager

client = Client('AbEIrslVmOD7sSL4qwEUiuDIsD1DxG7LT9b5ODmMmZemvQotxDaRX1kGzgggwPUu',
                'VLXzhtrihiC8nZnB4uZlj1qi3YqN4bGJKjJO8hv4ZULw54BGPPwNBjTPbnhuDg36')


class BnbWssClient:

    def __init__(self):
        bm = BinanceSocketManager(client)
        bm.start_aggtrade_socket('BNBBTC', process_message)
        bm.start()


def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)
    # do something


if __name__ == '__main__':
    # bm = BinanceSocketManager(client)
    # bm.start_aggtrade_socket('BNBBTC', process_message)
    # bm.start()
    klines = client.get_aggregate_trades(symbol="ethusdt", limit=1)
    print(json.dumps(klines))
