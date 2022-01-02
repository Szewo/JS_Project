from tkinter import *


class View:
    def __init__(self, root):
        self.root = root

    def setup(self):
        self.root.title("Automat z napojami")
        self.root.geometry("800x600")


    def main_gui(self):
        shelf1 = Frame(master=self.root, height=150)
        shelf1.pack(fill=X)
        self.product(shelf1, "Produkt1", "30", "5").grid(column=0, row=0)
        self.product(shelf1, "Produkt2", "30", "5").grid(column=1, row=0)
        self.product(shelf1, "Produkt3", "30", "5").grid(column=2, row=0)
        self.product(shelf1, "Produkt4", "30", "5").grid(column=3, row=0)
        self.product(shelf1, "Produkt5", "30", "5").grid(column=4, row=0)

    def product(self, master, product_name, product_number, quantity):
        frame = Frame(master=master, height=150, padx=15)
        product_label = Label(master=frame, text=product_name)
        product_info = Label(master=frame, text="Numer produktu " + product_number)
        product_quantity = Label(master=frame, text="Ilość produktu " + quantity)
        product_label.grid(column=0, row=0, columnspan=3)
        product_info.grid(column=0, row=1, columnspan=2)
        product_quantity.grid(column=0, row=2)
        return frame

    def loop(self):
        self.root.mainloop()
