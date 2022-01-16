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
        self.__coins = {value: 0 for value in consts.AVAILABLE_COINS}

    def get_coins(self):
        """Zwraca słownik z monetami.

        :return: słownik z monetami.
        """
        return self.__coins

    def add_coin(self, coin: Coin):
        """Dodaje monetę do słownika.

        :param coin: moneta do dodania.
        """
        self.__coins[str(coin.get_value())] += 1

    def get_coin(self, value):
        """Zwraca przechowaną monetę o danym nominale.

        Jeśli ilość monet o danym nominale wynosi zero, rzuca wyjątek.
        :param value: nominał monety,
        :return: moneta.
        """
        if not self.__coins[str(value)]:
            raise Exception(str(value) + ' coin not available')

        self.__coins[value] -= 1
        return Coin(value)

    def reset_coins(self):
        """Zeruje ilości przechowywanych monet."""
        self.__coins = {value: 0 for value in consts.AVAILABLE_COINS}

    def sum_of_coins(self):
        """Zwraca sumę nominałów wszystkich przechowywanych monet.

        :return: suma nominałów monet.
        """
        total = 0
        for value, quantity in self.__coins.items():
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
        added.__coins = {value: self.__coins[value] + other.__coins[value]
                         for value in consts.AVAILABLE_COINS}
        return added


class VendingMachine:
    """Przechowuje stan automatu."""
    def __init__(self):
        """Inicjalizuje stan automatu."""
        self.__available_coins = CoinsHolder()
        self.__inserted_coins = CoinsHolder()
        self.__product_number = ""
        self.__message = ""
        self.__available_products = {}
        for name, number, price in consts.PRODUCTS:
            self.__available_products[number] = Product(name, number, price)

    def get_available_coins(self):
        """Zwraca słownik z monetami dostępnymi w automacie.

        :return: słonwik z dostępnymi monetami.
        """
        return self.__available_coins

    def get_available_products(self):
        """Zwraca słownik z dostępnymi produktami.

        :return: słownik z dostępnymi produktami.
        """
        return self.__available_products

    def get_message(self):
        """Zwraca aktualny komunikat.

        :return: komunikat.
        """
        return self.__message

    def get_product_number(self):
        """Zwraca wybrany numer produktu.

        :return: numer produktu.
        """
        return self.__product_number

    def get_money(self):
        """Zwraca sumę wrzuconych monet.

        :return: suma wrzuconych monet.
        """
        return self.__inserted_coins.sum_of_coins()

    def add_credit(self, coin: Coin):
        """Obsługuje wrzucenie monety.

        :param coin: wrzucona moneta.
        """
        self.__inserted_coins.add_coin(coin)

    def reset_coins(self):
        """Obsługuje anulowanie transakcji.

        Dokonywane poprzez wyrzucenie wrzuconych monet.
        """
        self.__inserted_coins.reset_coins()
        self.__message = "Anulowano transakcje"

    def pick_product(self, val):
        """Obsługuje proces wpisywania numeru produktu.

        :param val: wybrana cyfra,
        :return: numer produktu.
        """
        if len(self.__product_number) < 2:
            self.__product_number += val
        else:
            self.__product_number = val
        return self.__product_number

    def buy_product(self):
        """Obsługuje proces zakupu produktu.

        :return: informacja, czy zakup się powiódł.
        """
        if self.__product_number not in self.__available_products.keys():
            self.__message = "Brak produktu o takim numerze"
            return False

        product = self.__available_products[self.__product_number]

        if product.get_price() > float(self.__inserted_coins.sum_of_coins()):
            self.__message = "Za mało kredytów, cena produktu: " + str(product.get_price())
            return False

        if product.get_quantity() <= 0:
            self.__message = "Brak produktu"
            return False

        return self.__give_rest(product)
    
    def __give_rest(self, product):
        rest = abs(round(self.__inserted_coins.sum_of_coins() - Decimal(product.get_price()), 2))
        original_rest = rest
        combined_coins = self.__available_coins + self.__inserted_coins

        for value in reversed(consts.AVAILABLE_COINS):
            value = Decimal(value)
            while value <= rest:
                try:
                    combined_coins.get_coin(str(value))
                    rest -= value
                except Exception:
                    break

        if rest > 0.:
            self.__message = "Tylko odliczona kwota"
            return False

        self.__available_coins = combined_coins
        self.__message = "Dokonano zakupu za " + str(product.get_price()) + ". Reszta: " + str(original_rest)
        self.__inserted_coins.reset_coins()
        product.remove()
        return True
