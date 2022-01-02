from View import *


def main():
    root = Tk()
    view = View(root)
    view.setup()
    view.main_gui()
    view.loop()


if __name__ == '__main__':
    main()
