

class Product:
    def __init__(self, name, number, price, quantity=5):
        self.__name = name
        self.__number = number
        self.__quantity = quantity
        self.__price = price

    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def remove(self):
        if self.__quantity > 0:
            self.__quantity -= 1
