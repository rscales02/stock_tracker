import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import numpy as np

from function.stock_editor import StockEditor


class DisplayGraphs:
    """
    Compute graphs to display
    """
    def __init__(self):
        self.stock_pickle = pd.read_pickle(os.path.join('data/stock.pkl'))
        self.crypto_pickle = pd.read_pickle(os.path.join('data/crypto.pkl'))
        self.stock_list, self.crypto_list = StockEditor().list_stocks()

    def return_and_log_return(self, stock, table):
        """
        Forgot where what I'm using this for...
        :param stock: yfinance stock ticker
        :param table: stock or crypto table
        :return:
        """
        stock_close = self.stock_pickle['Close']
        crypto_close = self.crypto_pickle['Close']
        stock_log_returns = np.log(stock_close).diff()
        crypto_log_returns = np.log(crypto_close).diff()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

        for c in stock_log_returns:
            ax1.plot(stock_log_returns.index, stock_log_returns[c].cumsum(), label=str(c))
            ax2.plot(stock_log_returns.index, 100 * (np.exp(stock_log_returns[c].cumsum()) - 1), label=str(c))

        for c in crypto_log_returns:
            ax1.plot(crypto_log_returns.index, crypto_log_returns[c].cumsum(), label=str(c))
            ax2.plot(crypto_log_returns.index, 100 * (np.exp(crypto_log_returns[c].cumsum()) - 1), label=str(c))

        ax1.set_ylabel('Cumulative log returns')
        ax1.legend(loc='best')

        ax2.set_ylabel('Total relative returns (%)')
        ax2.legend(loc='best')

        # plt.show()

    def candle_stick(self, stock, table):
        """
        create OHLC candle stick graph
        :param stock: yfinance stock symbol
        :param table: which table (Crypto/Stocks)
        :return: OHLCV Dataframe
        """
        if table == 'Stocks':
            pickle = self.stock_pickle
        else:
            pickle = self.crypto_pickle
        stock_ohlc = pd.DataFrame({
            "Open": pickle.Open[stock], "High": pickle.High[stock], "Low": pickle.Low[stock],
            "Close": pickle.Close[stock], "Volume": pickle.Volume[stock]
        })

        return stock_ohlc

    def total_val(self):
        """
        total val of portfolio by date
        :return: list of tuples (date, value) where date is calculated with mpl date2num
        """
        adj_val = self.stock_pickle['Adj Val'].copy().merge(self.crypto_pickle['Adj Val'], on='Date')
        total_val = (adj_val.sum(axis=1))
        return [(mpl_dates.date2num(k), total_val[k]) for k in total_val.keys()]
