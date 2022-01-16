"""Moduł graficzny projektu."""

import tkinter as tk

import consts
from Logic.coin import Coin
from Logic.vending_machine import VendingMachine

PRODUCT_QUANTITY_OFFSET = 30


class View:
    """Klasa obsługująca okno programu."""
    def __init__(self, root, vending_machine: VendingMachine):
        """Inicjalizuje dane okna programu.

        :param root: obiekt okna programu,
        :param vending_machine: obiekt automatu.
        """
        self.root = root
        self.vending_machine = vending_machine
        self.money = tk.DoubleVar()
        self.product_number = tk.IntVar()
        self.product_quantities = [tk.IntVar() for _ in range(21)]
        self.vending_machine_message = tk.StringVar()

    def add_money_to_machine(self, value):
        """Obsługuje wrzucanie monet do automatu.

        :param value: wybrana wartość.
        """
        self.vending_machine.add_credit(Coin(value))
        self.money.set(self.vending_machine.get_money())

    def pick_product(self, val):
        """Obsługuje wybór numeru produktu.

        :param val: wybrany numer.
        """
        self.vending_machine.pick_product(val)
        self.product_number.set(self.vending_machine.product_number)

    def reset_coins(self):
        """Obsługuje wyrzucenie wrzuconych monet."""
        self.vending_machine.reset_coins()
        self.money.set(self.vending_machine.get_money())

    def buy_product(self):
        """Obsługuje zatwierdzenie zakupu produktu."""
        result = self.vending_machine.buy_product()
        self.vending_machine_message.set(self.vending_machine.message)
        self.money.set(self.vending_machine.get_money())
        if result:
            current_quantity = self.product_quantities[
                self.product_number.get() - PRODUCT_QUANTITY_OFFSET].get()
            self.product_quantities[
                self.product_number.get() - PRODUCT_QUANTITY_OFFSET].set(current_quantity - 1)

    def setup(self):
        """Inicjalizuje parametry okna programu."""
        self.root.title("Automat z napojami")
        self.root.geometry("800x1000")
        self.root.resizable(False, False)

    def main_gui(self):
        """Inicjalizuje wygląd interfejsu użytkownika."""
        products_frame = tk.Frame(master=self.root, width=800)
        self.products(products_frame)
        products_frame.pack(fill=tk.X)

        screen_frame = tk.Frame(master=self.root, width=400, height=150)

        money_text = tk.Label(master=screen_frame, text='KREDYTY: ')
        money_label = tk.Label(master=screen_frame, textvariable=self.money)

        product_picker_text = tk.Label(master=screen_frame, text='PRODUKT: ')
        product_picker_label = tk.Label(master=screen_frame, textvariable=self.product_number)

        message_label = tk.Label(master=screen_frame)
        message_var = tk.Label(master=screen_frame, textvariable=self.vending_machine_message)

        money_label.grid(column=1, row=0, columnspan=3, sticky="W")
        money_text.grid(column=0, row=0, sticky="W")

        product_picker_text.grid(column=0, row=1, columnspan=3, sticky="W")
        product_picker_label.grid(column=1, row=1, sticky="W")

        message_label.grid(column=0, row=2, columnspan=3, sticky="W")
        message_var.grid(column=1, row=2, sticky="W")

        screen_frame.place(x=200, y=750)

        keyboard_frame = tk.Frame(master=self.root, width=200)
        self.keyboard(keyboard_frame)
        keyboard_frame.place(x=500, y=850)

        coins_frame = tk.Frame(master=self.root, width=200)
        self.coins(coins_frame)
        coins_frame.place(x=200, y=850)

    def keyboard(self, master):
        """Przygotowuje wygląd klawiatury do wyboru numeru produktu."""
        buttons = [tk.Button(master=master, text=num) for num in range(1, 10)]
        button_0 = tk.Button(master=master, text="0")
        button_ok = tk.Button(master=master, text="OK")

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
        button_ok.config(command=self.buy_product)

    def coins(self, master):
        """Przygotowuje wygląd klawiatury do wyboru wrzucanych monet."""
        buttons = [tk.Button(master=master, text=val + " PLN") for val in consts.AVAILABLE_COINS]
        button_reset = tk.Button(master=master, text="WYRZUĆ MONETY")

        buttons[0].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[0]))
        buttons[1].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[1]))
        buttons[2].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[2]))
        buttons[3].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[3]))
        buttons[4].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[4]))
        buttons[5].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[5]))
        buttons[6].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[6]))
        buttons[7].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[7]))
        buttons[8].config(command=lambda: self.add_money_to_machine(consts.AVAILABLE_COINS[8]))
        button_reset.config(command=self.reset_coins)

        for i, button in enumerate(buttons):
            button.grid(column=i % 3, row=int(i / 3) + 1, sticky="nsew")
        button_reset.grid(column=0, row=4, columnspan=3, sticky="nsew")

    def products(self, master):
        """Przygotowuje wygląd listy produktów do wyboru."""
        for i, product in enumerate(self.vending_machine.available_products.values()):
            self.product_quantities[i].set(product.get_quantity())
            self.product(master, product.get_name(), product.get_number(),
                         self.product_quantities[i], product.get_price()) \
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

    @staticmethod
    def product(master, product_name, product_number, quantity, price):
        """Przygotowuje wygląd pojedynczego okna produktu."""
        frame = tk.LabelFrame(master=master, text=product_name, height=150, padx=15, pady=5)
        product_info = tk.Label(master=frame, text="Numer produktu")
        product_quantity = tk.Label(master=frame, text="Ilość produktu")
        product_number_tx = tk.Label(master=frame, text=product_number)
        product_quantity_tx = tk.Label(master=frame, textvariable=quantity)
        product_price = tk.Label(master=frame, text="Cena produktu")
        product_price_tx = tk.Label(master=frame, text=price)

        product_info.grid(column=0, row=1, sticky=tk.W)
        product_quantity.grid(column=0, row=2, sticky=tk.W)
        product_number_tx.grid(column=1, row=1, padx=10)
        product_quantity_tx.grid(column=1, row=2, padx=10)
        product_price.grid(column=0, row=3, sticky=tk.W)
        product_price_tx.grid(column=1, row=3, padx=10)

        return frame

    def loop(self):
        """Główna pętla programu."""
        self.root.mainloop()
