"""Zawiera implementację klasy Coin."""

from decimal import Decimal


class Coin:
    """Przechowuje informacje o monecie."""
    def __init__(self, value):
        """Inicjalizuje dane monety.

        :param value: nominał
        """
        self.value = Decimal(str(value))

    def get_value(self) -> Decimal:
        """Zwraca nominał monety.

        :return: nominał
        """
        return self.value
