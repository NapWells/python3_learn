import _thread
import json
import time

import websocket
from websocket import create_connection

from service.handler import ResultHandler


class OkexWssClient:
    def __init__(self):
        self.ws = self.create_wss()

    def ping(self):
        result = self.ws.ping("{'event':'ping'}")
        if result is None or 'pong' not in result:
            self.__init__()
        time.sleep(30)

    @staticmethod
    def create_wss():
        while True:
            try:
                # ws = create_connection(url="wss://real.okcoin.com:10440/websocket/okcoinapi")
                ws = create_connection(url="wss://real.okex.com:10440/ws/v1", timeout=30, http_proxy_host='127.0.0.1',
                                       http_proxy_port='1080')
                # time.sleep(30)
                ping_result = ws.ping("{'event':'ping'}")
                result = ws.recv()
                print('connection successful')
                return ws
            except Exception:
                print('connect ws error,retry...')
                raise Exception

    def trade_detail(self, symbol, interval):
        trade_str = "{'event':'addChannel','channel':'ok_sub_spot_%(symbol)s_deals'}" % {'symbol': symbol}
        self.ws.send(trade_str)
        handler = ResultHandler(2, symbol)
        while True:
            # _thread.start_new_thread(self.ping())
            result = self.ws.recv()
            print(result)
            # result_json = json.loads(result)
            # if 'error_code' in result:
            #     print(result)
            #     return
            # if 'addChannel' in result:
            #     print('订阅成功：', trade_str)
            #     continue
            # if trade_str in result:
            #     handler.handle_result(result_json, interval)
            # else:
            #     print(result)


if __name__ == '__main__':
    client = OkexWssClient()
    client.trade_detail('eth_usd', 5)
