# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import kivy
from math import sin
import warnings

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.properties import ObjectProperty, ListProperty

from function.edit_stocks import StockEditor


kivy.require('1.10.0')


# Inherit Kivy's App class which represents the window
# for our widgets
# HelloKivy inherits all the fields and methods
# from Kivy
class EditModal(ModalView):
    def __init__(self):
        super(EditModal, self).__init__()
        self.add_widget(Label(text='Modal'))
        self.open()


class SearchBar(BoxLayout):
    def __init__(self):
        super(SearchBar, self).__init__()

    def on_press(self):
        text = self.ids.symbol.text
        EditModal()

    def clear_text(self):
        self.ids.symbol.text = ''


class StockList(BoxLayout):
    def __init__(self):
        super(StockList, self).__init__()
        editor = StockEditor()
        stocks, crypto = editor.list_stocks()

        # Produce key widget
        keys = stocks.keys()
        key_widget = BoxLayout()
        key_widget.add_widget(Label(text=keys[0]))
        key_widget.add_widget(Label(text=keys[1]))
        key_widget.add_widget(Label(text=keys[2]))

        # Add stocks list
        self.add_widget(Label(text="Stocks"))
        self.add_widget(key_widget)
        for i, stock in enumerate(stocks.values):
            new = Button()
            new.text = stock[0]
            new.id = stock[0]
            new.bind(on_press=self.on_press)

            self.add_widget(new)

        # Add crypto list
        self.add_widget(Label(text="Crypto"))
        for crypto in crypto.values:
            new = Button()
            new.text = crypto[0]
            new.id = crypto[0]
            new.bind(on_press=self.on_press)

            self.add_widget(new)

    def on_press(self, instance):
        print(instance.id)


class StockGraph(BoxLayout):
    def __init__(self):
        super(StockGraph, self).__init__()
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        graph.size_hint = 1, 3
        btn2 = Button(text='graph2')
        self.add_widget(graph)
        self.add_widget(btn2)


class StockApp(App):
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

        return root


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = StockApp()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
