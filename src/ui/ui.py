from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.front_view import FrontView
from services.services import (services as default_services)
from ui_config import APP_NAME


class UI:
    """Luokka huolehtii sovelluksen käyttöliittymästä.

    Attribuutit:
            _root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            _current_view: käyttöliittymän näyttämä näkymä
            _service: palvelu, joka vastaa sovellusksen toiminnasta
    """

    def __init__(self, root, service=default_services):
        """Alusta uusi käyttöliittymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            service: palvelu, joka vastaa sovellusksen toiminnasta
        """
        self._root = root
        self._current_view = None
        self._service = service

    def start(self):
        """Käyttöliittymän käynnistävä metodi"""
        window_width = int(self._root.winfo_screenwidth() * 0.5)
        window_height = int(self._root.winfo_screenheight() * 0.5)

        self._root.geometry(f"{window_width}x{window_height}")
        self._root.title(APP_NAME)

        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self):
        self._hide_current_view()
        self._current_view = LoginView(
            self._root,
            self._service.get_user_service(),
            self._show_create_user_view,
            self._show_front_view
        )
        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()
        self._current_view = CreateUserView(
            self._root,
            self._service.get_user_service(),
            self._show_login_view
        )
        self._current_view.pack()
    
    def _show_front_view(self):
        self._hide_current_view()
        self._current_view = FrontView(
            self._root,
            self._service,
        )
        self._current_view.pack()
