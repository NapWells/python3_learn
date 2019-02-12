import time
from datetime import datetime
from bitfinex import WssClient, ClientV2, ClientV1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Statistics:
    def __init__(self):
        self.client = ClientV2()

    @staticmethod
    def stats_params(symbol, side):
        PARAMS = {
            'key': 'pos.size',
            'size': '1m',
            'symbol': symbol,
            'section': 'hist',
            'sort': '0',
            'side': side
        }
        return PARAMS;

    def calculation(self, symbol):
        longs = self.client.stats(**self.stats_params(symbol, 'long'))
        shorts = self.client.stats(**self.stats_params(symbol, 'short'))
        longs.sort(key=lambda k: k[0])
        shorts.sort(key=lambda k: k[0])
        for (long, short) in zip(longs, shorts):
            rate = long[1] / (long[1] + short[1])
            date = datetime.fromtimestamp(long[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f'datatime=%s long=%f    short=%f   long/short = %f' % (date, long[1], short[1], rate))

        # fig, ax1 = plt.subplots(1, 1)  # 做1*1个子图，等价于 fig, ax1 = plt.subplot()
        # ax2 = ax1.twinx()  # 让2个子图轴一样；

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        long_df = pd.DataFrame(data=longs, columns=['datetime', 'value'])
        x_data = []
        for date in long_df['datetime'].values:
            x_data.append(datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d %H:%M:%S'))

        ax1.plot(x_data, long_df['value'].values, color='blue')
        plt.title('long/min  -- ' + symbol)

        ax2 = fig.add_subplot(2, 2, 2)
        short_df = pd.DataFrame(data=shorts, columns=['datetime', 'value'])

        ax2.plot(x_data, short_df['value'], color='red')
        plt.title('short/min  -- ' + symbol)

        ax3 = fig.add_subplot(2, 2, 3)
        long_rate = []
        long_short = []
        for (long, short) in zip(longs, shorts):
            rate = long[1] / (long[1] + short[1])
            long_rate.append(rate)
            long_short.append(long[1] / short[1])
        ax3.plot(x_data, long_rate, color='blue')
        plt.title('long-scale')

        ax4 = fig.add_subplot(2, 2, 4)
        ax4.plot(x_data, long_short)
        plt.title('long/short')
        plt.show()


if __name__ == '__main__':
    statistics = Statistics()
    statistics.calculation('tBTCUSD')
    statistics.calculation('tETHUSD')
    statistics.calculation('tXRPUSD')
    statistics.calculation('tEOSUSD')
    statistics.calculation('tLTCUSD')


