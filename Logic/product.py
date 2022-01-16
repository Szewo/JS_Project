"""Zawiera implementację klasy Product."""


class Product:
    """Przechowuje informacje o produkcie."""

    def __init__(self, name, number, price, quantity=5):
        """Inicjalizuje dane produktu.

        :param name: nazwa produktu,
        :param number: numer produktu,
        :param price: cena produktu,
        :param quantity: dostępna ilość produktu.
        """
        self.__name = name
        self.__number = number
        self.__quantity = quantity
        self.__price = price

    def get_name(self):
        """Zawraca nazwę produktu.

        :return: nazwa produktu.
        """
        return self.__name

    def get_number(self):
        """Zwraca numer produktu.

        :return: numer produktu.
        """
        return self.__number

    def get_price(self):
        """Zwraca cenę produktu.

        :return: cena produktu.
        """
        return self.__price

    def get_quantity(self):
        """Zwraca dostępną ilość produktu.

        :return: dostępna ilość produktu.
        """
        return self.__quantity

    def remove(self):
        """Zmniejsza ilość produktu o 1."""
        if self.__quantity > 0:
            self.__quantity -= 1
