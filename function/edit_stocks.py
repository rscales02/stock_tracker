from pandas import DataFrame as dF, read_csv as read
import os


class StockEditor:
    def __init__(self):
        self.crypto = read(os.path.relpath('data/crypto.csv'), index_col=0)
        self.stocks = read(os.path.join('data/stocks.csv'), index_col=0)

    def list_stocks(self):
        return self.stocks, self.crypto

    def edit_stock(self, file):
        # edit purchase price or quantity of a stock
        stocks = read(file, index_col=0)
        symbol = input('Please enter ticker to edit: ("q" to Quit) ').lower()
        if symbol == 'q':
            return
        to_edit = stocks[stocks['Symb'] == symbol].index
        if to_edit.empty:
            print('Symbol not found, please try again')
            self.edit_stock()
            return

        what_edit = input('Do you want to edit "Quantity" or "Price" or "Quit"? ').lower()
        quantity = float(input('Please input new total: '))
        if what_edit == 'q':
            stocks.loc[to_edit, 'Quantity'] = quantity
        elif what_edit == 'p':
            stocks.loc[to_edit, 'Price'] = quantity
        else:
            print('Invalid entry, please try again')
            self.edit_stock()
            return

        stocks.to_csv(file)

    def delete_stock(self, file):
        # remove stock info from stocks.csv
        symbol = input('Please enter stock ticker to delete: ').upper()
        stocks = self.stocks
        to_drop = stocks[stocks['Symbol'] == symbol].index
        stocks = stocks.drop(labels=to_drop, axis=0)
        stocks.to_csv(file)

    def add_stock(self, file):
        # add current stock positions to file
        symbol = input('Please enter stonk ticker: ').upper()
        quantity = float(input('Please enter stonk quantity: '))
        price = float(input('Please enter stock share price: '))
        new_stock = dF([{'Symbol': symbol, 'Price': price, 'Quantity': quantity}])

        try:
            stocks = self.stocks
            stocks = stocks.append(new_stock, ignore_index=True)
            stocks.to_csv(file)
        except IOError:
            stocks = new_stock
            stocks.to_csv(file)

    def invalid_entry(self, file):
        print('Invalid entry, please try again')
