# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from layout.searchbar import SearchBar
from layout.stocklist import StockList
from layout.stockgraph import StockGraph
from function.stock_grabber import stock_grabber

kivy.require('2.0.0')


class StockApp(App):
    """
    A basic stock tracker
    """
    title = "Stocks, Bitch"

    # This returns the content we want in the window
    def build(self):
        # Build and return StockApp layout widget
        root = FloatLayout()
        root.title = self.title

        search = SearchBar()
        root.add_widget(search)

        stock_list = StockList()
        root.add_widget(stock_list)

        graph = StockGraph()
        root.add_widget(graph)
        stock_grabber()
        return root


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = StockApp()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
