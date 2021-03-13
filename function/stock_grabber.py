from pandas_datareader import data
import pandas as pd

from datetime import date


def get_stock_df():
    # return list of stock tickers saved
    return pd.read_csv('../data/stocks.csv'), pd.read_csv('../data/crypto.csv')


def get_ticker_info():
    # retrieve ticker info
    stock, crypto = get_stock_df()
    stock_list = stock.Symb.values
    crypto_list = crypto.Symb.values
    start = date(2017, 1, 1)
    end = date.today()
    stock_ticker = data.DataReader(stock_list, 'yahoo', start=start, end=end)
    crypto_ticker = data.DataReader(crypto_list, 'yahoo', start=start, end=end)
    stock_ticker.to_pickle('stock_ticker.pkl')
    crypto_ticker.to_pickle('crypto_ticker.pkl')
    weighted_ratio()
    return stock_ticker


def closing_val():
    # add and update portfolio values based on last Close Price
    pickle = pd.read_pickle('ticker.pkl')
    close = pickle['Close']
    stocks = pd.read_csv('../data/stocks.csv', index_col=0)
    close_vals = [stocks.Quantity[stocks.Stock == symb].values[0] * close.tail(1)[symb].values[0] for symb in
                  stocks.Stock]
    return close_vals
    # stocks['Closing Val'] = close_vals
    # stocks.to_csv('stocks.csv')


def weighted_ratio():
    # Total percent of portfolio as rated by Closing Val
    close = closing_val()
    stocks = pd.read_csv('../data/stocks.csv', index_col=0)
    total = sum(close)
    ratio = close / total
    stocks['% Total Val'] = ratio
    print(stocks)
    stocks.to_csv('stocks.csv')
