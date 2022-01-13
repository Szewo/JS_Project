from View import *
from VendingMachine import *


def main():
    root = Tk()
    vending_machine = VendingMachine()
    view = View(root, vending_machine)
    view.setup()
    view.main_gui()
    view.loop()


if __name__ == '__main__':
    main()
