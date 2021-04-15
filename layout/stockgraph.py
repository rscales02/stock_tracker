import os
import mplfinance as mpf
import matplotlib as mpl

import matplotlib.pyplot as plt

from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import LinePlot
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from function.stock_editor import StockEditor
from function.display_graphs import DisplayGraphs

from kivy.properties import ObjectProperty

mpl.use("module://kivy.garden.matplotlib.backend_kivy")

Builder.load_file(os.path.join('layout/kv_layout/stockgraph.kv'))


class StockGraph(BoxLayout):
    """
    Displays the graphs
    on start graph == total portfolio value / time
    TODO: integrate OHLCV candlestick for each stock
    TODO: Integrate log returns
    """
    graph = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(StockGraph, self).__init__(**kwargs)
        # DisplayGraphs()
        self.plot = None
        self.total_value_plot()

    def total_value_plot(self):
        """
        display total value of stocks
        :return: none
        """
        self.plot = LinePlot(color=[0, 1, 0, 1])
        self.plot.points = DisplayGraphs().total_val()
        self.ids.graph.add_plot(self.plot)

    def candle_stick_plot(self, stock, table):
        """
        Display OHLC candlestick graph
        :param stock: stock symbol
        :param table: Stocks/Crypto
        :return: None
        """
        self.ids.graph.remove_plot(self.plot)
        points = DisplayGraphs().candle_stick(stock, table)
        # self.plot = mpf.plot(points, type='candle', title=stock, figsize=(1, 1), volume=True)

        fig, ax = plt.subplot()
        # fig.size = 0.75, 0.75

        # Setting labels & titles
        ax.set_xlabel('Date')
        self.plot.ylabel('Price')
        # sticks = mpf.plot(points, type='candle', title=stock, figsize=(1, 1), volume=True)
        # print(sticks.__sizeof__())
        # plot.points = sticks
        self.add_widget(FigureCanvasKivyAgg(figure=fig))

    def on_press(self):
        """
        TODO: Volume? another graph? remove to make graph larger?
        currently prints the
        :return:
        """
        stocks, crypto = StockEditor().list_stocks()
        print(DisplayGraphs().total_val())
