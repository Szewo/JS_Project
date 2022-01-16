from tkinter import *

import Coin
import VendingMachine
import consts

PRODUCT_QUANTITY_OFFSET = 30


class View:
    def __init__(self, root, vending_machine: VendingMachine.VendingMachine):
        self.root = root
        self.vending_machine = vending_machine
        self.money = DoubleVar()
        self.product_number = IntVar()
        self.product_quantities = [IntVar() for i in range(21)]
        self.vending_machine_message = StringVar()

    def add_money_to_machine(self, value):
        self.vending_machine.add_credit(Coin.Coin(value))
        self.money.set(self.vending_machine.get_money())

    def pick_product(self, val):
        self.vending_machine.pick_product(val)
        self.product_number.set(self.vending_machine.product_number)

    def reset_coins(self):
        self.vending_machine.reset_coins()
        self.money.set(self.vending_machine.get_money())

    def buy_product(self):
        result = self.vending_machine.buy_product()
        self.vending_machine_message.set(self.vending_machine.message)
        self.money.set(self.vending_machine.get_money())
        if result:
            current_quantity = self.product_quantities[self.product_number.get() - PRODUCT_QUANTITY_OFFSET].get()
            self.product_quantities[self.product_number.get() - PRODUCT_QUANTITY_OFFSET].set(current_quantity - 1)

    def setup(self):
        self.root.title("Automat z napojami")
        self.root.geometry("800x1000")
        self.root.resizable(False, False)

    def main_gui(self):
        products_frame = Frame(master=self.root, width=800)
        self.products(products_frame)
        products_frame.pack(fill=X)

        screen_frame = Frame(master=self.root, width=400, height=150)

        money_text = Label(master=screen_frame, text='KREDYTY: ')
        money_label = Label(master=screen_frame, textvariable=self.money)

        product_picker_text = Label(master=screen_frame, text='PRODUKT: ')
        product_picker_label = Label(master=screen_frame, textvariable=self.product_number)

        message_label = Label(master=screen_frame)
        message_var = Label(master=screen_frame, textvariable=self.vending_machine_message)

        money_label.grid(column=1, row=0, columnspan=3, sticky="W")
        money_text.grid(column=0, row=0, sticky="W")

        product_picker_text.grid(column=0, row=1, columnspan=3, sticky="W")
        product_picker_label.grid(column=1, row=1, sticky="W")

        message_label.grid(column=0, row=2, columnspan=3, sticky="W")
        message_var.grid(column=1, row=2, sticky="W")

        screen_frame.place(x=200, y=750)

        keyboard_frame = Frame(master=self.root, width=200)
        self.keyboard(keyboard_frame)
        keyboard_frame.place(x=500, y=850)

        coins_frame = Frame(master=self.root, width=200)
        self.coins(coins_frame)
        coins_frame.place(x=200, y=850)

    def keyboard(self, master):
        buttons = [Button(master=master, text=num) for num in range(1, 10)]
        button_0 = Button(master=master, text="0")
        button_ok = Button(master=master, text="OK")

        for i, button in enumerate(buttons):
            button.grid(column=i % 3, row=int(i / 3) + 1, sticky="nsew")
        button_0.grid(column=0, row=4, sticky="nsew")
        button_ok.grid(column=1, columnspan=2, row=4, sticky="nsew")

        buttons[0].config(command=lambda: self.pick_product("1"))
        buttons[1].config(command=lambda: self.pick_product("2"))
        buttons[2].config(command=lambda: self.pick_product("3"))
        buttons[3].config(command=lambda: self.pick_product("4"))
        buttons[4].config(command=lambda: self.pick_product("5"))
        buttons[5].config(command=lambda: self.pick_product("6"))
        buttons[6].config(command=lambda: self.pick_product("7"))
        buttons[7].config(command=lambda: self.pick_product("8"))
        buttons[8].config(command=lambda: self.pick_product("9"))
        button_0.config(command=lambda: self.pick_product("0"))
        button_ok.config(command=lambda: self.buy_product())

    def coins(self, master):
        buttons = [Button(master=master, text=value + " PLN") for value in consts.AVAILABLE_COINS]
        button_reset = Button(master=master, text="WYRZUĆ MONETY")

        buttons[0].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[0]))
        buttons[1].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[1]))
        buttons[2].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[2]))
        buttons[3].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[3]))
        buttons[4].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[4]))
        buttons[5].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[5]))
        buttons[6].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[6]))
        buttons[7].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[7]))
        buttons[8].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[8]))
        button_reset.config(command=lambda: self.reset_coins())

        for i, button in enumerate(buttons):
            button.grid(column=i % 3, row=int(i / 3) + 1, sticky="nsew")
        button_reset.grid(column=0, row=4, columnspan=3, sticky="nsew")

    def products(self, master):

        for i, product in enumerate(self.vending_machine.available_products.values()):
            self.product_quantities[i].set(product.get_quantity())
            self.product(master, product.get_name(), product.get_number(), self.product_quantities[i],
                         product.get_price()) \
                .grid(column=i % 3, row=int(i / 3), padx=15, pady=5, sticky="nsew")

        master.columnconfigure(0, weight=2)
        master.columnconfigure(1, weight=2)
        master.columnconfigure(2, weight=2)

        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)
        master.rowconfigure(4, weight=1)
        master.rowconfigure(5, weight=1)
        master.rowconfigure(6, weight=1)

    def product(self, master, product_name, product_number, quantity, price):
        frame = LabelFrame(master=master, text=product_name, height=150, padx=15, pady=5)
        product_info = Label(master=frame, text="Numer produktu")
        product_quantity = Label(master=frame, text="Ilość produktu")
        product_number_tx = Label(master=frame, text=product_number)
        product_quantity_tx = Label(master=frame, textvariable=quantity)
        product_price = Label(master=frame, text="Cena produktu")
        product_price_tx = Label(master=frame, text=price)

        product_info.grid(column=0, row=1, sticky=W)
        product_quantity.grid(column=0, row=2, sticky=W)
        product_number_tx.grid(column=1, row=1, padx=10)
        product_quantity_tx.grid(column=1, row=2, padx=10)
        product_price.grid(column=0, row=3, sticky=W)
        product_price_tx.grid(column=1, row=3, padx=10)

        return frame

    def loop(self):
        self.root.mainloop()
