from ui.start_view import StartView
from ui.create_user_view import CreateUserView

class UI:
    """Luokka huolehtii sovelluksen käyttöliittymästä.

    Attribuutit:
            _root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            _current_view: käyttöliittymän näyttämä näkymä
            _service: palvelu, joka vastaa sovellusksen toiminnasta
    """

    def __init__(self, root, service):
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
        self._show_start_view()
    
    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_start_view(self):
        self._current_view = StartView(
            self._root,
            self._show_create_user_view
        )
        self._current_view.pack()
    
    def _show_create_user_view(self):
        self._hide_current_view()
        self._current_view = CreateUserView(
            self._root,
            self._service.get_user_service(),
            self._show_start_view()
        )
        self._current_view.pack()
        