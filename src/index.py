from tkinter import Tk
from ui.ui import UI
from services.complete_services import Services
import config_ui

def main():
    window = Tk()

    services = Services()

    ui_view = UI(root=window, service=services, config=config_ui)
    ui_view.start()

    window.mainloop()


if __name__ == "__main__":
    main()
