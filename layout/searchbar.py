import os

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from layout.editmodal import EditModal

Builder.load_file(os.path.join('layout/kv_layout/searchbar.kv'))


class SearchBar(BoxLayout):
    """
    bottom search box for searching stock database.  Opens modal for add/edit/delete
    """
    def __init__(self, **kwargs):
        super(SearchBar, self).__init__(**kwargs)

    def on_press(self):
        symbol = self.ids.symbol.text.upper()
        EditModal(symbol)

    def clear_text(self):
        self.ids.symbol.text = ''
