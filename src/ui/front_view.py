from tkinter import ttk, constants, StringVar


class FrontView:
    """Luokka vastaa sovelluksen etusivusta käyttäjän kirjauduttua.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _services: toiminnoista vastaava olio
            _new_project: uuden hankkeen luomisnäkymä
            _back_to_login: metodi, joka palauttaa kirjautumisnäkymän
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksen näyttämisestä vastaava Label-olio
            _user (User): istunnon haltijan käyttäjäolio
    """

    def __init__(self, root, services, back_to_login, new_project):
        """Luo kirjautuneen etusivu.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            services: toiminnoista vastaava olio
            back_to_login: metodi, joka palauttaa kirjautumisnäkymän
            new_project: uuden hankkeen luomisnäkymä
        """
        self._root = root
        self._services = services
        self._back_to_login = back_to_login
        self._new_project = new_project
        self._frame = None
        self._error_variable = None
        self._error_label = None
        self._user = None

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

    def _logout_handler(self):
        self._services.get_user_service().logout()
        self._back_to_login()

    def _initialize_header(self):
        user_label = ttk.Label(
            master=self._frame,
            text=f"Olet kirjautunut sisään nimellä {self._user.username}."
        )
        user_label.grid(
            padx=5,
            pady=5,
            sticky=constants.W
        )

        logout_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu ulos",
            command=self._logout_handler
        )
        logout_button.grid(
            padx=5,
            pady=10,
            sticky=constants.EW
        )

        new_project_button = ttk.Button(
            master=self._frame,
            text="Luo maailma",
            command=self._new_project
        )
        new_project_button.grid(
            padx=5,
            pady=10,
            sticky=constants.EW
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_error()

        try:
            self._user = self._services.get_user_service().get_current_user()

            self._initialize_header()

            greeting = ttk.Label(
                master=self._frame,
                text=f"Tervetuloa {self._user.username}!",
                anchor="center"
            )

            self._frame.grid_columnconfigure(1, weight=1)

            greeting.grid(
                column=1,
                padx=5,
                pady=5,
                sticky=(constants.NS, constants.EW)
            )
        except self._services.get_user_service().get_exceptions().NoSessionFound as e:
            self._show_error(e.message)

        self._hide_error()
