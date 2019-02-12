import itertools
import time
from datetime import datetime
import pandas as pd
import json

from service import Util
from service.Util import db


class ResultHandler:
    def __init__(self, exchange, symbol):
        self.exchange = exchange  # 交易所类型
        self.symbol = symbol  # 类型
        self.amount = 0  # 成交量
        self.count = 0  # 成交笔数
        self.open = 0  # 开盘价
        self.close = 0  # 收盘价
        self.low = 0  # 最低价,
        self.high = 0  # 最高价
        self.vlo = 0  # 成交额
        self.buy_amount = 0  # 买盘成交量
        self.buy_count = 0  # 买盘成交笔数
        self.buy_vlo = 0  # 买盘成交额
        self.sell_amount = 0  # 卖盘成交量
        self.sell_count = 0  # 卖盘成交笔数
        self.sell_vlo = 0  # 卖盘成交额
        self.time = datetime.fromtimestamp(time.time())
        self.df = pd.DataFrame()

    def save(self):
        # print('----------------------------------start----------------------------------')
        if self.df.size is not 0 and self.df.empty is False:
            self.low = self.df[self.df['price'] == self.df['price'].min()]['price'].values[0]
            self.high = self.df[self.df['price'] == self.df['price'].max()]['price'].values[0]
            self.count = self.df.shape[0]
            self.amount = self.df['amount'].sum()
            self.open = self.df[self.df['ts'] == self.df['ts'].min()]['price'].values[0]
            self.close = self.df[self.df['ts'] == self.df['ts'].max()]['price'].values[0]
            self.vlo = self.df.apply(lambda x: x['price'] * x['amount'], axis=1).sum()
            self.buy_vlo = self.df.apply(lambda x: x['price'] * x['amount'] if x['direction'] == 'buy' else 0,
                                         axis=1).sum()
            self.buy_amount = self.df.apply(lambda x: x['amount'] if x['direction'] == 'buy' else 0, axis=1).sum()
            self.buy_count = self.df[self.df['direction'] == 'buy'].shape[0]
            self.sell_vlo = self.df.apply(lambda x: x['price'] * x['amount'] if x['direction'] == 'sell' else 0,
                                          axis=1).sum()
            self.sell_count = self.df[self.df['direction'] == 'sell'].shape[0]
            self.sell_amount = self.df.apply(lambda x: x['amount'] if x['direction'] == 'sell' else 0, axis=1).sum()
            params = {
                'low': self.low,
                'high': self.high,
                'count': self.count,
                'amount': self.amount,
                'open': self.open,
                'close': self.close,
                'vlo': self.vlo,
                'buy_vlo': self.buy_vlo,
                'buy_amount': self.buy_amount,
                'buy_count': self.buy_count,
                'sell_vlo': self.sell_vlo,
                'sell_count': self.sell_count,
                'sell_amount': self.sell_amount,
                'exchange': self.exchange,
                'symbol': self.symbol,
                'time': self.time.strftime('%Y-%m-%d %H:%M:%S')
            }

            db.insert(params)
        # print('----------------------------------end----------------------------------')

    def handle_result(self, result, interval):
        if self.exchange == 1:
            self.huobi_handler(result, interval)
        if self.exchange == 2:
            self.okex_handler(result, interval)
        if self.exchange == 3:
            self.bnb_handler(result, interval)
        if self.exchange == 4:
            self.bitfinex_handler(result, interval)

    def huobi_handler(self, result_json, interval):
        timestamp = result_json['ts'] / 1000
        result_time = datetime.fromtimestamp(timestamp)
        if result_time.minute % interval == 0 and result_time.minute != self.time.minute:
            self.save()
            self.__init__(self.exchange, self.symbol)
        self.time = result_time
        datas = result_json['tick']['data']
        self.df = self.df.append(pd.DataFrame(datas), ignore_index=True)

    def okex_handler(self, result_json, interval):
        pass

    def bnb_handler(self, result, interval):
        datas = []
        date = None
        for data in result:
            price = data['p']
            amount = data['q']
            date = ts = data['T']
            direction = 'sell'
            if data['m'] is True:
                direction = 'buy'

            timestamp = date / 1000
            result_time = datetime.fromtimestamp(timestamp)
            if result_time.minute % interval == 0 and result_time.minute != self.time.minute:
                self.save()
                datas.clear()
                self.__init__(self.exchange, self.symbol)
            self.time = result_time
            row = {
                "amount": float(amount),
                "ts": ts,
                "price": float(price),
                "direction": direction
            }
            datas.append(row)
            self.df = self.df.append(pd.DataFrame(datas), ignore_index=True)

    def bitfinex_handler(self, result, interval):
        datas = []
        date = None
        for data in result:
            date = data['timestamp']
            timestamp = date
            result_time = datetime.fromtimestamp(timestamp)
            if result_time.minute % interval == 0 and result_time.minute != self.time.minute:
                self.df.rename(columns={'type': 'direction', 'timestamp': 'ts'}, inplace=True)
                self.df['price'] = self.df['price'].astype(float)
                self.df['amount'] = self.df['amount'].astype(float)
                self.save()
                datas.clear()
                self.__init__(self.exchange, self.symbol)
            self.time = result_time
            datas.append(data)
            self.df = self.df.append(pd.DataFrame(datas), ignore_index=True)


if __name__ == '__main__':
    # datas = [{
    #         "amount": 0.025000000000000000,
    #         "ts": 1546066325278,
    #         "id": 3444996958720658021134,
    #         "price": 3841.960000000000000000,
    #         "direction": "buy"
    #     }, {
    #         "amount": 0.001200000000000000,
    #         "ts": 1546066324108,
    #         "id": 3444996787320658020357,
    #         "price": 3841.360000000000000000,
    #         "direction": "sell"
    #     }]
    #
    #     datas2 = [{
    #         "amount": 0.002000000000000000,
    #         "ts": 1546066313268,
    #         "id": 3444995275520658010546,
    #         "price": 3841.300000000000000000,
    #         "direction": "sell"
    #     }]
    #
    #     df = pd.DataFrame(datas).append(datas2, ignore_index=True)
    #     df['price'] = df['price'].astype(str)
    #     print(df[df['price'] == df['price'].min()]['price'].values[0])

    datas = [{
        "timestamp": 1546581843,
        "tid": 329956380,
        "price": "3939.9",
        "amount": 0.005,
        "exchange": "bitfinex",
        "type": "sell"
    }, {
        "timestamp": 1546581841,
        "tid": 329956380,
        "price": "3939.9",
        "amount": 0.003,
        "exchange": "bitfinex",
        "type": "sell"
    }]
    datas.sort(key=lambda k: (k.get('timestamp', 0)))
    df = pd.DataFrame(datas)
    df.replace(df['amount'].values,12,inplace=True)
    values = []
    for value in df['amount'].values:
        values.append(value * 10)
    df.replace(df['amount'].values.tolist(),values,inplace=True)
    print(df)
