import os

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior, ButtonBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from kivy.properties import StringProperty

from layout.stockgraph import StockGraph


from function.stock_editor import StockEditor


Builder.load_file(os.path.join('layout/kv_layout/stocklist.kv'))


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    pass


class RecycleButton(RecycleDataViewBehavior, ButtonBehavior, BoxLayout):
    """ Add selection support to the Label """
    id = StringProperty('')
    price = StringProperty('')
    quantity = StringProperty('')
    table = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(RecycleButton, self).__init__(*args, **kwargs)

    def on_press(self):
        """
        switch graph to OHLC candlestick for specific stock clicked from list
        :return:
        """
        StockGraph().candle_stick_plot(self.id, self.table)


class Stocks(RecycleView):
    """
    TODO: update list upon DB update
    """
    def __init__(self, **kwargs):
        """
        scrollable list view of stocks to display (stock, quantity, price)
        :param kwargs:
        """
        super(Stocks, self).__init__(**kwargs)

        stocks, crypto = StockEditor().list_stocks()
        self.data = [{'id': stock[0], 'quantity': str(stock[1]), 'price': str(stock[2]), 'table': 'Stocks'} for stock
                     in stocks]


class Crypto(RecycleView):
    def __init__(self, **kwargs):
        """
        scrollable list view of crypto to display (crypto, quantity, price)
        :param kwargs:
        """
        super(Crypto, self).__init__(**kwargs)

        stocks, crypto = StockEditor().list_stocks()
        self.data = [{'id': stock[0], 'quantity': str(stock[1]), 'price': str(stock[2]), 'table': 'Crypto'} for stock in
                     crypto]


class StockList(BoxLayout):
    def __init__(self):
        super(StockList, self).__init__()
