from tkinter import ttk, constants, StringVar


class FrontView:
    """Luokka vastaa sovelluksen etusivusta käyttäjän kirjauduttua.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: toiminnoista vastaava olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
    """

    def __init__(self, root, service):
        """Luo kirjautuneen etusivu.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
        """
        self._root = root
        self._service = service
        self._frame = None
        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Poistaa näkymän."""
        self._frame.destroy()
    
    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove() 

    def _initialize(self):
        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(master=self._frame,
                                      textvariable=self._error_variable,
                                      foreground="red"
                                      )
        
        if self._service.get_user_service().get_current_user():
            self._frame = ttk.Frame(master=self._root)

            greeting = ttk.Label(master=self._frame, text=f"Tervetuloa {self._service.get_user_service().get_current_user().username}!")
            
            greeting.grid(padx=5, pady=5)
        else:
            self._show_error("Istuntoa ei löydy.")

        self._hide_error()
