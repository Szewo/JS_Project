from decimal import Decimal


class VendingMachine:
    def __init__(self):
        self.money = Decimal('0')

    def get_money(self):
        return self.money

    def add_credit(self, amount):
        self.money += Decimal(str(amount))
