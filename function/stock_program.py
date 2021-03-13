from pandas import read_csv as read

from function.stock_grabber import get_ticker_info
from function.display_graphs import display_graphs
# from edit_stocks import edit


def list_stocks():
    try:
        print('Stocks: \n', read('../data/stocks.csv', index_col=0))
        print('Crypto: \n', read('../data/crypto.csv', index_col=0))
    except FileNotFoundError as e:
        print(e)
    return read('../data/stocks.csv', index_col=0)


def invalid_entry():
    print('Invalid entry, please try again')


def stock_program():
    while True:
        choice = input('Please select "Edit", "Graph", "List", "Ticker" or "exit": ')
        switcher = {
            'l': list_stocks,
            # 'e': edit,
            't': get_ticker_info,
            'g': display_graphs,
            'exit': exit,
        }
        switcher.get(choice, invalid_entry)()

