import json
from websocket import create_connection
import gzip

from service.handler import ResultHandler


class HuobiWssClient:
    def __init__(self):
        self.count = 0
        self.success = 0
        self.ws = self.connection()

    def connection(self):
        try:
            self.count += 1
            self.ws = create_connection(url="wss://api.huobipro.com/ws", timeout=30, http_proxy_host='127.0.0.1',
                                   http_proxy_port='1080')
            print('connection successful')
            self.success += 1
        except Exception:
            print('connect ws error,retry...')
            raise Exception

    def trade_detail(self, symbol, interval):
        while True:
            try:
                trade_str = """{"sub": "market.%(symbol)s.trade.detail","id": "id10"}""" % {'symbol': (symbol + 'usdt')}
                self.ws.send(trade_str)
                trade_id = ''
                handler = ResultHandler(1, symbol)
                while (1):
                    compress_data = self.ws.recv()
                    result = gzip.decompress(compress_data).decode('utf-8')
                    if result[:7] == '{"ping"':
                        ts = result[8:21]
                        pong = '{"pong":' + ts + '}'
                        self.ws.send(pong)
                        self.ws.send(trade_str)
                    else:
                        try:
                            if trade_id == result['data']['id']:
                                print('重复的id')
                                break
                            else:
                                trade_id = result['data']['id']
                        except Exception:
                            pass

                        # print( result)
                        result_json = json.loads(result)
                        if 'status' in result_json and result_json['status'] == 'ok':
                            continue
                        if 'tick' in result_json and result_json['tick'] != None:
                            handler.handle_result(result_json, interval)
                        else:
                            print(result)

            except Exception as e:
                print(f'第%d次链接'%self.count)
                self.connection()


huobiWssClient = HuobiWssClient()
