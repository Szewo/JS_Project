from tkinter import *
from Product import *


class View:
    def __init__(self, root, vending_machine):
        self.root = root
        self.vending_machine = vending_machine
        self.vending_machine_money = DoubleVar()

    def add_money_to_machine(self, value):
        self.vending_machine.add_credit(value)
        self.vending_machine_money.set(self.vending_machine.get_money())



    def setup(self):
        self.root.title("Automat z napojami")
        self.root.geometry("800x1000")
        self.root.resizable(False, False)

    def main_gui(self):
        products_frame = Frame(master=self.root, width=800)
        self.products(products_frame)
        products_frame.pack(fill=X)

        screen_frame = Frame(master=self.root, width=400, height=150, bg="blue")
        money_text = Label(master=screen_frame, text='KREDYTY: ')
        money_label = Label(master=screen_frame, textvariable=self.vending_machine_money)
        money_label.grid(column=1, row=0, columnspan=3)
        money_text.grid(column=0, row=0)

        screen_frame.place(x=200, y=600)

        keyboard_frame = Frame(master=self.root, width=200)
        self.keyboard(keyboard_frame)
        keyboard_frame.place(x=500, y=780)

        coins_frame = Frame(master=self.root, width=200)
        self.coins(coins_frame)
        coins_frame.place(x=200, y=780)

    def keyboard(self, master):
        buttons = [
            Button(master=master, text="1"),
            Button(master=master, text="2"),
            Button(master=master, text="3"),
            Button(master=master, text="4"),
            Button(master=master, text="5"),
            Button(master=master, text="6"),
            Button(master=master, text="7"),
            Button(master=master, text="8"),
            Button(master=master, text="9"),
        ]
        for i, button in enumerate(buttons):
            button.grid(column=i % 3, row=int(i / 3) + 1, sticky="nsew")

        Button(master=master, text="0").grid(column=0, row=4, sticky="nsew")
        Button(master=master, text="R").grid(column=2, row=4, sticky="nsew")

    def coins(self, master):
        buttons = [
            Button(master=master, text="0.01 PLN"),
            Button(master=master, text="0.02 PLN"),
            Button(master=master, text="0.05 PLN"),
            Button(master=master, text="0.10 PLN"),
            Button(master=master, text="0.20 PLN"),
            Button(master=master, text="0.50 PLN"),
            Button(master=master, text="1.00 PLN"),
            Button(master=master, text="2.00 PLN"),
            Button(master=master, text="5.00 PLN"),
        ]

        buttons[0].config(command=lambda: self.add_money_to_machine(0.01))
        buttons[1].config(command=lambda: self.add_money_to_machine(0.02))
        buttons[2].config(command=lambda: self.add_money_to_machine(0.05))
        buttons[3].config(command=lambda: self.add_money_to_machine(0.10))
        buttons[4].config(command=lambda: self.add_money_to_machine(0.20))
        buttons[5].config(command=lambda: self.add_money_to_machine(0.50))
        buttons[6].config(command=lambda: self.add_money_to_machine(1.00))
        buttons[7].config(command=lambda: self.add_money_to_machine(2.00))
        buttons[8].config(command=lambda: self.add_money_to_machine(5.00))

        for i, button in enumerate(buttons):
            button.grid(column=i % 3, row=int(i / 3) + 1, sticky="nsew")

    def products(self, master):
        products_list = [
            Product("Produkt1", 30),
            Product("Produkt2", 31),
            Product("Produkt3", 32),
            Product("Produkt4", 33),
            Product("Produkt5", 34),
            Product("Produkt6", 35),
            Product("Produkt7", 36),
            Product("Produkt8", 37),
            Product("Produkt9", 38),
            Product("Produkt10", 39),
            Product("Produkt11", 40),
            Product("Produkt12", 41),
            Product("Produkt13", 42),
            Product("Produkt14", 43),
            Product("Produkt15", 44),
            Product("Produkt16", 45),
            Product("Produkt17", 46),
            Product("Produkt18", 47),
            Product("Produkt19", 48),
            Product("Produkt20", 49),
            Product("Produkt21", 50),
        ]
        for i, product in enumerate(products_list):
            self.product(master, product.product_name, product.product_number, product.product_quantity) \
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

    def product(self, master, product_name, product_number, quantity):
        frame = LabelFrame(master=master, text=product_name, height=150, padx=15, pady=5)
        product_info = Label(master=frame, text="Numer produktu")
        product_quantity = Label(master=frame, text="Ilość produktu")
        product_number_tx = Label(master=frame, text=product_number)
        product_quantity_tx = Label(master=frame, text=quantity)

        product_info.grid(column=0, row=1, sticky=W)
        product_quantity.grid(column=0, row=2, sticky=W)
        product_number_tx.grid(column=1, row=1, padx=10)
        product_quantity_tx.grid(column=1, row=2, padx=10)

        return frame

    def loop(self):
        self.root.mainloop()
