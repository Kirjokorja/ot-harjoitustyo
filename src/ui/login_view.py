from tkinter import ttk, constants, StringVar


class LoginView:
    """Luokka vastaa sovelluksen kirjautumisnäkymästä.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _user_service: käyttäjätoiminnoista vastaava olio
            _create_user_view: käyttäjänluontinäkymä
            _front_view: seovelluksen etusivu kirjauduttua
            _username (Entry): Entry-olio, joka säilyttää käyttäjän antaman käyttäjätunnuksen
            _password (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan 
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksen näyttämisestä vastaava Label-olio
    """

    def __init__(self, root, user_service, create_user_view, front_view):
        """Luo kirjautumisnäkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            user_service: käyttäjätoiminnoista vastaava olio
            create_user_view: käyttäjänluontinäkymä
            front_view: seovelluksen etusivu kirjauduttua
        """
        self._root = root
        self._user_service = user_service
        self._create_user_view = create_user_view
        self._front_view = front_view
        self._frame = None
        self._username = None
        self._password = None
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

    def _login_handler(self):
        self._hide_error()
        username = self._username.get()
        password = self._password.get()

        try:
            self._user_service.login(username, password)
            self._front_view()
        except self._user_service.get_exceptions().InvalidCredentials as e:
            self._show_error(e.message)

    def _initialize_error(self):
        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red",
            anchor="center"
        )
        self._error_label.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.grid_rowconfigure(0, weight=30)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_rowconfigure(4, weight=1)
        self._frame.grid_rowconfigure(5, weight=1)
        self._frame.grid_rowconfigure(6, weight=1)
        self._frame.grid_rowconfigure(7, weight=1)
        self._frame.grid_rowconfigure(8, weight=1)
        self._frame.grid_rowconfigure(9, weight=30)

        self._frame.grid_columnconfigure(0, weight=5)
        self._frame.grid_columnconfigure(1, weight=2)
        self._frame.grid_columnconfigure(2, weight=5)

    def _initialize_login_fields(self):
        username_label = ttk.Label(
            master=self._frame,
            text="Käyttäjänimi:"
        )
        username_label.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )
        self._username = ttk.Entry(master=self._frame)
        self._username.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        password_label = ttk.Label(
            master=self._frame,
            text="Salasana:"
        )
        password_label.grid(
            row=5,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )
        self._password = ttk.Entry(master=self._frame, show="*")
        self._password.grid(
            row=6,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        login_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu",
            command=self._login_handler
        )
        login_button.grid(
            row=7,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

    def _initialize_create_user(self):
        create_user_button = ttk.Button(
            master=self._frame,
            text="Rekisteröidy",
            command=self._create_user_view
        )
        create_user_button.grid(
            row=8,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

    def _initialize(self):
        self._initialize_frame()

        self._initialize_error()

        greeting = ttk.Label(
            master=self._frame,
            text="Tervetuloa!",
            anchor="center"
        )
        greeting.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        self._initialize_login_fields()

        self._initialize_create_user()

        self._hide_error()
