import os

from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.lang import Builder

from function.stock_editor import StockEditor

Builder.load_file(os.path.join('layout/kv_layout//editmodal.kv'))


class EditModal(ModalView):
    """
    Modal to add and edit stock positions
    TODO: update adjusted cost basis of stocks with new purchase
    """
    def __init__(self, symbol, **kwargs):
        super(EditModal, self).__init__(**kwargs)
        ids = self.ids
        ids.symbol.text = symbol

        self.editor = StockEditor()
        stocks, crypto = self.editor.list_stocks()
        stock = [stock for stock in stocks if symbol in stock]
        crypt = [stock for stock in crypto if symbol in stock]

        edit = Button(text='Edit')
        edit.id = 'edit'
        edit.bind(on_press=self.on_press)
        delete = Button(text='Delete')
        delete.id = 'delete'
        delete.bind(on_press=self.on_press)
        add = Button(text='Add')
        add.id = 'add'
        add.bind(on_press=self.on_press)

        if bool(stock):
            ids.price.text = str(stock[0][2])
            ids.quantity.text = str(stock[0][1])
            self.ids.modal.add_widget(edit)
            self.ids.modal.add_widget(delete)
        elif bool(crypt):
            ids.price.text = str(crypt[0][2])
            ids.quantity.text = str(crypt[0][1])
            ids.crypto.active = True
            self.ids.modal.add_widget(edit)
            self.ids.modal.add_widget(delete)
        else:
            ids.modal.add_widget(add)

        self.open()

    def on_press(self, instance):
        """
        :param instance: action id from button (add / delete / edit)
        :return: None
        """
        action = instance.id
        ids = self.ids
        crypto = ids.crypto.active
        symbol = ids.symbol.text.upper()
        quantity = float(ids.quantity.text)
        price = float(ids.price.text)
        table = 'Crypto' if crypto else 'Stocks'
        action_string = '_stock("{}", "{}", "{}", "{}")'.format(table, symbol, quantity, price)
        eval('self.editor.' + action + action_string)

        self.editor.close()

        self.dismiss()
