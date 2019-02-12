from flask import Flask, jsonify, request
from huobi.websocket.HuobiWssClient import huobiWssClient
from bnb.api.BinanceClient import bnbRestClient
from bitflx.api.bitflnex_client import bitfinexClient
import json
import _thread

app = Flask(__name__)
knows_symbol = ['btc', 'eth', 'xrp', 'ltc', 'dash']
working_symbol = []
working_exchange = []


@app.route('/task/create', methods=['POST'])
def create_task():
    values = request.get_json()
    require = ['symbol', 'exchange', 'interval']
    if values is None or not all(k in values for k in require):
        return 'Missing values', 400

    symbol = values['symbol']
    exchange = values['exchange']
    if symbol.lower() not in knows_symbol:
        return 'unknown symbol :' + symbol, 400

    if symbol in working_symbol and exchange in working_exchange:
        return 'working symbol:' + symbol, 400

    working_symbol.append(symbol)
    working_exchange.append(exchange)

    if exchange == 1:
        _thread.start_new_thread(huobiWssClient.trade_detail, (symbol, values['interval']))

    if exchange == 3:
        _thread.start_new_thread(bnbRestClient.trade_detail, (symbol, values['interval']))

    if exchange == 4:
        _thread.start_new_thread(bitfinexClient.trade_detail, (symbol, values['interval']))

    response = {
        'status': True,
        'params': json.dumps(values),
        'message': 'success'
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999)
