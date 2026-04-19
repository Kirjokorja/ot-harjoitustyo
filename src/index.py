from tkinter import Tk
from ui.ui import UI
from services.complete_services import Services


def main():
    window = Tk()

    services = Services()

    ui_view = UI(window, services)
    ui_view.start()

    window.mainloop()


if __name__ == "__main__":
    main()
