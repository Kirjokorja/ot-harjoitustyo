from tkinter import Tk
from ui.ui import UI
from services.services import Services
from database.db import DatabaseInterface
from repositories.repositories import Repositories
from config import DATABASE_FILE_PATH
import exceptions.exceptions as exceptions

def main():
    window = Tk()
    window.title("Maailmasampo")

    database = DatabaseInterface(DATABASE_FILE_PATH)
    repositories = Repositories(database)
    services = Services(repositories, exceptions)

    ui_view = UI(window, services)
    ui_view.start()

    window.mainloop()

if __name__ == "__main__":
    main()
