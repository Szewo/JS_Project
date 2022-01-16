"""Moduł obsługujący logikę automatu."""

from decimal import Decimal

import consts
from Logic.coin import Coin
from Logic.product import Product


class CoinsHolder:
    """Klasa służąca do przechowywania monet."""
    def __init__(self):
        """Inicjalizuje słownik z monetami.

        Kluczami są nominały monet, a wartości to odpowiednie liczby przechowywanych monet.
        """
        self.coins = {value: 0 for value in consts.AVAILABLE_COINS}

    def get_coins(self):
        """Zwraca słownik z monetami.

        :return: słownik z monetami.
        """
        return self.coins

    def add_coin(self, coin: Coin):
        """Dodaje monetę do słownika.

        :param coin: moneta do dodania.
        """
        self.coins[str(coin.get_value())] += 1

    def get_coin(self, value):
        """Zwraca przechowaną monetę o danym nominale.

        Jeśli ilosć monet o danym nominale wynosi zero, rzuca wyjątek.
        :param value: nominał monety,
        :return: moneta.
        """
        if not self.coins[str(value)]:
            raise Exception(str(value) + ' coin not available')

        self.coins[value] -= 1
        return Coin(value)

    def reset_coins(self):
        """Zeruje ilości przechowywanych monet."""
        self.coins = {value: 0 for value in consts.AVAILABLE_COINS}

    def sum_of_coins(self):
        """Zwraca sumę nominałów wszystkich przechowywanych monet.

        :return: suma nominałów monet.
        """
        total = 0
        for value, quantity in self.coins.items():
            total += quantity * Decimal(value)

        return total

    def __add__(self, other):
        """Dodaje dwa obiekty typu CoinHolder.

        Nie modyfikuje dodawanych obiektów.
        :param other: obiekt do dodania,
        :return: nowy obiekt CoinHolder ze zsumowanymi monetami.
        """
        if not isinstance(other, CoinsHolder):
            raise Exception('Unable to add different types.')

        added = CoinsHolder()
        added.coins = {value: self.coins[value] + other.coins[value]
                       for value in consts.AVAILABLE_COINS}
        return added


class VendingMachine:
    """Przechowuje stan automatu."""
    def __init__(self):
        """Inicjalizuje stan automatu."""
        self.available_coins = CoinsHolder()
        self.inserted_coins = CoinsHolder()
        self.product_number = ""
        self.message = ""
        self.available_products = {}
        for name, number, price in consts.PRODUCTS:
            self.available_products[number] = Product(name, number, price)

    def get_money(self):
        """Zwraca sumę wrzuconych monet.

        :return: suma wrzuconych monet.
        """
        return self.inserted_coins.sum_of_coins()

    def add_credit(self, coin: Coin):
        """Obsługuje wrzucenie monety.

        :param coin: wrzucona moneta.
        """
        self.inserted_coins.add_coin(coin)

    def reset_coins(self):
        """Obsługuje anulowanie transakcji.

        Dokonywane poprzez wyrzucenie wrzuconych monet.
        """
        self.inserted_coins.reset_coins()
        self.message = "Anulowano transakcje"

    def pick_product(self, val):
        """Obsługuje proces wpisywania numeru produktu.

        :param val: wybrana cyfra,
        :return: numer produktu.
        """
        if len(self.product_number) < 2:
            self.product_number += val
        else:
            self.product_number = val
        return self.product_number

    def buy_product(self):
        """Obsługuje proces zakupu produktu.

        :return: informacja, czy zakup się powiódł.
        """
        if self.product_number not in self.available_products.keys():
            self.message = "Brak produktu o takim numerze"
            return False

        product = self.available_products[self.product_number]

        if product.get_price() > float(self.inserted_coins.sum_of_coins()):
            self.message = "Za mało kredytów, cena produktu: " + str(product.get_price())
            return False

        if product.get_quantity() <= 0:
            self.message = "Brak produktu"
            return False

        rest = abs(round(self.inserted_coins.sum_of_coins() - Decimal(product.get_price()), 2))
        copy = rest
        returned_coins = []
        combined_coins = self.available_coins + self.inserted_coins

        for value in reversed(consts.AVAILABLE_COINS):
            value = Decimal(value)
            while value <= rest:
                try:
                    returned_coins.append(combined_coins.get_coin(str(value)))
                    rest -= value
                except Exception:
                    break

        if rest > 0.:
            for coin in returned_coins:
                self.available_coins.add_coin(coin)
            self.message = "Tylko odliczona kwota"
            return False

        self.available_coins = combined_coins
        self.message = "Dokonano zakupu za " + str(product.get_price()) + ". Reszta: " + str(copy)
        self.inserted_coins.reset_coins()
        product.remove()
        return True
