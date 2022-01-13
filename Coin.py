from decimal import Decimal


class Coin:
    def __init__(self, value):
        self.value = Decimal(str(value))

    def get_value(self) -> Decimal:
        return self.value
