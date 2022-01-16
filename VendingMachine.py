import decimal

import Coin
import Product
import consts


class CoinsHolder:
    def __init__(self):
        self.coins = {value: 0 for value in consts.AVAILABLE_COINS}

    def get_coins(self):
        return self.coins

    def add_coin(self, coin: Coin.Coin):
        self.coins[str(coin.get_value())] += 1

    def get_coin(self, value):
        if not self.coins[str(value)]:
            raise Exception(str(value) + ' coin not available')

        self.coins[value] -= 1
        return Coin.Coin(value)

    def reset_coins(self):
        self.coins = {value: 0 for value in consts.AVAILABLE_COINS}

    def sum_of_coins(self):
        total = 0
        for value, quantity in self.coins.items():
            total += quantity * decimal.Decimal(value)

        return total

    def __add__(self, other):
        if not isinstance(other, CoinsHolder):
            raise Exception('Error')

        added = CoinsHolder()
        added.coins = {value: self.coins[value] + other.coins[value] for value in consts.AVAILABLE_COINS}
        return added


class VendingMachine:
    def __init__(self):
        self.available_coins = CoinsHolder()
        self.inserted_coins = CoinsHolder()
        self.product_number = ""
        self.message = ""
        self.available_products = {}
        for name, number, price in consts.PRODUCTS:
            self.available_products[number] = Product.Product(name, number, price)

    def get_money(self):
        return self.inserted_coins.sum_of_coins()

    def add_credit(self, coin: Coin.Coin):
        self.inserted_coins.add_coin(coin)

    def reset_coins(self):
        self.inserted_coins.reset_coins()
        self.message = "Anulowano transakcje"

    def pick_product(self, val):
        if len(self.product_number) < 2:
            self.product_number += val
        else:
            self.product_number = val
        return self.product_number

    def buy_product(self):
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

        rest = abs(round(self.inserted_coins.sum_of_coins() - decimal.Decimal(product.get_price()), 2))
        copy = rest
        returned_coins = []
        combined_coins = self.available_coins + self.inserted_coins

        for value in reversed(consts.AVAILABLE_COINS):
            value = decimal.Decimal(value)
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

