"""Moduł testujący działanie programu."""

import unittest
from decimal import Decimal

from Logic.coin import Coin
from Logic.vending_machine import VendingMachine


class VendingMachineTests(unittest.TestCase):

    def setUp(self) -> None:
        self.vending_machine = VendingMachine()

    def test_product_price(self):
        price = self.vending_machine.available_products['30'].get_price()
        self.assertEqual(price, 0.25)

    def test_buy_product_without_rest(self):
        self.vending_machine.add_credit(Coin('0.20'))
        self.vending_machine.add_credit(Coin('0.02'))
        self.vending_machine.add_credit(Coin('0.02'))
        self.vending_machine.add_credit(Coin('0.01'))
        self.vending_machine.pick_product('3')
        self.vending_machine.pick_product('0')
        self.assertTrue(self.vending_machine.buy_product())
        self.assertIn('Reszta: 0.00', self.vending_machine.message)

    def test_buy_with_rest(self):
        # Product number 44, price 2.79
        self.vending_machine.available_coins.add_coin(Coin('0.01'))
        self.vending_machine.available_coins.add_coin(Coin('0.10'))
        self.vending_machine.available_coins.add_coin(Coin('0.10'))
        self.vending_machine.available_coins.add_coin(Coin('0.20'))
        self.assertEqual(self.vending_machine.available_coins.sum_of_coins(), Decimal('0.41'))

        self.vending_machine.add_credit(Coin('1.00'))
        self.vending_machine.add_credit(Coin('2.00'))
        self.vending_machine.pick_product('4')
        self.vending_machine.pick_product('4')
        self.assertTrue(self.vending_machine.buy_product())
        self.assertIn('Reszta: 0.21', self.vending_machine.message)
        self.assertEqual(self.vending_machine.available_coins.sum_of_coins(), Decimal('3.20'))

    def test_buy_all_products(self):
        # Product number 49, price 0.01
        self.vending_machine.pick_product('4')
        self.vending_machine.pick_product('9')

        for i in range(5):
            self.vending_machine.add_credit(Coin('0.01'))
            self.assertTrue(self.vending_machine.buy_product())

        self.vending_machine.add_credit(Coin('0.01'))
        self.assertFalse(self.vending_machine.buy_product())
        self.assertIn('Brak produktu', self.vending_machine.message)

    def test_pick_wrong_product_number(self):
        self.vending_machine.pick_product('1')
        self.assertFalse(self.vending_machine.buy_product())
        self.assertIn('Brak produktu o takim numerze', self.vending_machine.message)

        self.vending_machine.pick_product('5')
        self.vending_machine.pick_product('3')
        self.assertFalse(self.vending_machine.buy_product())
        self.assertIn('Brak produktu o takim numerze', self.vending_machine.message)

    def test_cancel_transaction(self):
        self.vending_machine.add_credit(Coin('1.00'))
        self.vending_machine.add_credit(Coin('0.50'))
        self.vending_machine.add_credit(Coin('5.00'))
        self.vending_machine.add_credit(Coin('0.02'))

        self.assertEqual(self.vending_machine.get_money(), Decimal('6.52'))
        self.vending_machine.reset_coins()
        self.assertIn("Anulowano transakcje", self.vending_machine.message)
        self.assertEqual(self.vending_machine.get_money(), Decimal('0.00'))

    def test_add_more_money(self):
        # 47, 11.35
        self.vending_machine.add_credit(Coin('5.00'))
        self.vending_machine.add_credit(Coin('1.00'))
        self.vending_machine.add_credit(Coin('0.20'))
        self.assertEqual(self.vending_machine.get_money(), Decimal('6.20'))
        self.vending_machine.pick_product('4')
        self.vending_machine.pick_product('7')
        self.assertFalse(self.vending_machine.buy_product())
        self.assertIn('Za mało kredytów', self.vending_machine.message)

        self.vending_machine.add_credit(Coin('5.00'))
        self.vending_machine.add_credit(Coin('0.10'))
        self.vending_machine.add_credit(Coin('0.05'))
        self.assertEqual(self.vending_machine.get_money(), Decimal('11.35'))
        self.vending_machine.pick_product('4')
        self.vending_machine.pick_product('7')
        self.assertTrue(self.vending_machine.buy_product())
        self.assertIn('Reszta: 0.00', self.vending_machine.message)

    def test_100_0_01_coins(self):
        for i in range(100):
            self.vending_machine.add_credit(Coin('0.01'))

        self.assertEqual(self.vending_machine.get_money(), Decimal('1.00'))

    def test_unable_to_give_rest(self):
        # 39, 0.99
        self.vending_machine.add_credit(Coin('1.00'))
        self.vending_machine.pick_product('3')
        self.vending_machine.pick_product('9')
        self.assertFalse(self.vending_machine.buy_product())
        self.assertIn('Tylko odliczona kwota', self.vending_machine.message)


if __name__ == '__main__':
    unittest.main()
