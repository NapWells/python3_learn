from huobi.websocket.HuobiWssClient import huobiWssClient
from bnb.api.BinanceClient import bnbRestClient
from bitflx.api.bitflnex_client import bitfinexClient
import _thread

if __name__ == '__main__':
    symbol, interval = 'btc',5
    _thread.start_new_thread(huobiWssClient.trade_detail, (symbol, interval))
    _thread.start_new_thread(bnbRestClient.trade_detail, (symbol, interval))
    _thread.start_new_thread(bitfinexClient.trade_detail, (symbol, interval))