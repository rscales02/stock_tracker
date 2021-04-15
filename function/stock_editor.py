import os

import sqlite3
from pandas_datareader import DataReader as data
from pandas_datareader._utils import RemoteDataError
from datetime import date


class StockEditor:
    """
    An editor to add, remove, or update stock info in SQLite
    """
    # TODO what to do on exception
    # TODO weighted avg of purchases
    # TODO what to do on check fail

    def __init__(self):
        self.conn = self.connect()
        self.create_tables()

    def create_tables(self):
        """
        Initialize DB tables
        :return: None
        """
        tables = ['Crypto', 'Stocks']
        for name in tables:
            cursor = self.conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS %s (Symbol CHAR(8) NOT NULL UNIQUE, Quantity FLOAT, Price FLOAT);" % name)
            self.conn.commit()
            cursor.close()

    def close(self):
        self.conn.close()

    @staticmethod
    def connect():
        """
        connect to database
        :return: None
        """
        try:
            conn = sqlite3.connect(os.path.join('data/stocks.db'))
            return conn
        except ConnectionError as e:
            print(e)

    def list_stocks(self):
        """
        List stocks from DB (Symbol, Quantity, Price)
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Stocks")
        stocks = cursor.fetchall()
        cursor.execute("SELECT * FROM Crypto")
        crypto = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return stocks, crypto

    def edit_stock(self, table, symbol, quantity, price):
        """
        Edit stocks in DB
        :param table: which DB table (stocks/crypto)
        :param symbol: yfinance symbol
        :param quantity: number of units owned
        :param price: price per unit
        :return: none
        """
        cursor = self.conn.cursor()
        params = (quantity, price, symbol)
        try:
            cursor.execute(
                "UPDATE {} SET Quantity=?, Price=? WHERE Symbol=?".format(table), params
            )
        except sqlite3.IntegrityError as e:
            print('failed to edit', e)

        self.conn.commit()
        cursor.close()

    def delete_stock(self, table, symbol, *args):
        """
        Delete stock from database
        :param table: DB table (stock/crypto)
        :param symbol: yfinance symbol
        :return: None
        """
        cursor = self.conn.cursor()
        print(table, symbol)
        try:
            cursor.execute(
                "DELETE FROM {} WHERE Symbol=?".format(table), (symbol,)
            )
        except sqlite3.IntegrityError as e:
            print('failed to delete', e)

        self.conn.commit()
        cursor.close()

    def add_stock(self, table, symbol, quantity, price):
        """
        Add new stock position to database
        :param table: which DB table (crypto/stock)
        :param symbol: yfinance symbol
        :param quantity: number of shares purchased
        :param price: purchase price
        :return: None
        """
        cursor = self.conn.cursor()
        if self.symbol_check(symbol):
            params = (symbol, quantity, price)
            try:
                cursor.execute(
                    "INSERT INTO {} (Symbol, Quantity, Price) VALUES (?, ?, ?)".format(table), params
                )
            except sqlite3.IntegrityError as e:
                print('failed to add', e)
        else:
            print('invalid symbol')
            return
        self.conn.commit()
        cursor.close()

    @staticmethod
    def symbol_check(symbol):
        """
        TODO: add invalid symbol popup / chance to edit
        check validity of input symbol with data retrieval tool
        :param symbol: Stock symbol as found on yfinance
        :return: True if data returns
        """
        start = date(2021, 1, 1)
        end = date.today()
        try:
            print('symbol check')
            info = data(symbol, 'yahoo', start, end)
            if not info.empty:
                return True
        except RemoteDataError as e:
            return False
