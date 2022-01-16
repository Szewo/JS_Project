"""Moduł uruchamiający program."""

import tkinter as tk

from View.view import View
from Logic.vending_machine import VendingMachine


def main():
    """Uruchamia główną pętlę programu."""
    root = tk.Tk()
    vending_machine = VendingMachine()
    view = View(root, vending_machine)
    view.setup()
    view.main_gui()
    view.loop()


if __name__ == '__main__':
    main()
