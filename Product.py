

class Product:
    def __init__(self, name, number, price, quantity=5):
        self.name = name
        self.number = number
        self.quantity = quantity
        self.price = price

    def get_name(self):
        return self.name

    def get_number(self):
        return self.number

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity
