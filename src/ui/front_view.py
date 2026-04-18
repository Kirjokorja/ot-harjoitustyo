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
        self._frame.pack(fill="both", expand=True)

    def destroy(self):
        """Poistaa näkymän."""
        self._frame.destroy()

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_error(self):
        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )
        self._error_label.grid(padx=5, pady=5)

    def _initialize(self):
        self._initialize_error()

        self._frame = ttk.Frame(master=self._root)

        try:
            user = self._service.get_user_service().get_current_user()
            greeting = ttk.Label(
                master=self._frame, 
                text=f"Tervetuloa {user.username}!", 
                anchor="center"
            )

            self._frame.grid_columnconfigure(1, weight=1)

            greeting.grid(
                column=1, 
                padx=5, 
                pady=5,
                sticky=(constants.NS, constants.EW)
            )
        except self._service.get_user_service().get_exceptions().NoSessionFound as e:
            self._show_error(e.message)

        self._hide_error()
