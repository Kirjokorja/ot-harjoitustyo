from tkinter import Tk
from ui.ui import UI
from services.services import Services

def main():
    window = Tk()
    window.title("Maailmasampo")

    services = Services()

    ui_view = UI(window, services)
    ui_view.start()

    window.mainloop()

if __name__ == "__main__":
    main()
