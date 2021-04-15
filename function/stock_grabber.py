from pandas_datareader import DataReader as Data
import pandas
import os

from datetime import date

from function.stock_editor import StockEditor


def stock_grabber():
    """
    Take list of stocks and retrieve stock data using P DataReader, save as a .pkl file
    :return: None
    """
    stocks, crypto = StockEditor().list_stocks()
    stock_list = [stock[0] for stock in stocks]
    crypto_list = [crypt[0] for crypt in crypto]
    start = date(2020, 1, 1)
    end = date.today()
    if not os.path.join('data/stock.pkl'):
        stock_ticker = Data(stock_list, 'yahoo', start, end)
        stock_pickle = add_adj_value(stock_ticker)
        crypto_ticker = Data(crypto_list, 'yahoo', start, end)
        stock_pickle.to_pickle(os.path.join('data/stock.pkl'))
        crypto_pickle = add_adj_value(crypto_ticker)
        crypto_pickle.to_pickle(os.path.join('data/crypto.pkl'))


def add_adj_value(data):
    """
    Add column Adj Val (Adj Close * # of Stock) to stock data
    :param data: results from pandas data reader (Pandas Dataframe)
    :return: results from PDR + Adj Val Column (Pandas Dataframe)
    """
    pickle = data.copy()
    adj_close = pickle['Adj Close']

    # get list of stocks [(symbol, quantity, price), ...]
    stocks, crypto = StockEditor().list_stocks()
    if stocks[0][0] in adj_close:
        data_list = stocks
    elif crypto[0][0] in adj_close:
        data_list = crypto
    else:
        print('Stock ticker not available')
    adj_val = pandas.DataFrame()
    for i, stock in enumerate(data_list):
        adj_val.insert(loc=i, column=('Adj Val', stock[0]), value=adj_close[stock[0]] * stock[1])
    pickle = pickle.merge(adj_val, on='Date')

    return pickle
