from tkinter import ttk, constants, StringVar


class CreateUserView:
    """Luokka vastaa sovelluksen käyttäjänluontinäkymästä.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _user_service: käyttäjätoiminnoista vastaava olio
            _back_to_start_view: metodi, joka palauttaa alkunäkymän
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _username (Entry): Entry-olio, joka säilyttää käyttäjän antaman käyttäjätunnuksen
            _password (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan 
            _password_confirm (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan tarkistusta varten
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
    """

    def __init__(self, root, user_service, back_to_start_view, ):
        """Alusta käyttäjänluontinäkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            user_service: käyttäjätoiminnoista vastaava olio
            back_to_start_view: metodi, joka palauttaa alkunäkymän
        """
        self._root = root
        self._user_service = user_service
        self._back_to_start_view = back_to_start_view
        self._frame = None
        self._username = None
        self._password = None
        self._password_confirm = None
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

    def _create_user_handler(self):
        self._hide_error()
        username = self._username.get()
        password = self._password.get()
        password_confirm = self._password_confirm.get()

        try:
            self._user_service.create_user(
                username, password, password_confirm)
            self._back_to_start_view()
        except (self._user_service.get_exceptions().UserAlreadyExists,
                self._user_service.get_exceptions().UsernameTooShort,
                self._user_service.get_exceptions().PasswordTooShort,
                self._user_service.get_exceptions().PasswordsDoNotMatch) as e:
            self._show_error(e.message)

    def _initialize_error(self):
        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(master=self._frame,
                                      textvariable=self._error_variable,
                                      foreground="red",
                                      anchor="center"
                                      )
        self._error_label.grid(row=1, column=1, padx=5,
                               pady=5, sticky=(constants.NS, constants.EW))

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root, style="TFrame")

        self._frame.grid_rowconfigure(0, weight=30)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_rowconfigure(4, weight=1)
        self._frame.grid_rowconfigure(5, weight=1)
        self._frame.grid_rowconfigure(6, weight=1)
        self._frame.grid_rowconfigure(7, weight=1)
        self._frame.grid_rowconfigure(8, weight=1)
        self._frame.grid_rowconfigure(10, weight=30)

        self._frame.grid_columnconfigure(0, weight=5)
        self._frame.grid_columnconfigure(1, weight=2)
        self._frame.grid_columnconfigure(2, weight=5)

    def _initialize_login_fields(self):
        username_label = ttk.Label(master=self._frame, text="Käyttäjänimi:")
        username_label.grid(row=2, column=1, padx=5, pady=5,
                            sticky=(constants.NS, constants.W))
        self._username = ttk.Entry(master=self._frame)
        self._username.grid(row=3, column=1, padx=5, pady=5,
                            sticky=(constants.NS, constants.EW))

        password_label = ttk.Label(
            master=self._frame, text=f"Salasana (min {self._user_service.get_min_password_lenght()} merkkiä):")
        password_label.grid(row=4, column=1, padx=5, pady=5,
                            sticky=(constants.NS, constants.W))
        self._password = ttk.Entry(master=self._frame, show="*")
        self._password.grid(row=5, column=1, padx=5, pady=5,
                            sticky=(constants.NS, constants.EW))

        password_confirm_label = ttk.Label(
            master=self._frame, text="Salasana uudestaan:")
        password_confirm_label.grid(
            row=6, column=1, padx=5, pady=5, sticky=(constants.NS, constants.W))
        self._password_confirm = ttk.Entry(master=self._frame, show="*")
        self._password_confirm.grid(
            row=7, column=1, padx=5, pady=5, sticky=(constants.NS, constants.EW))

        create_user_button = ttk.Button(master=self._frame,
                                        text="Luo",
                                        command=self._create_user_handler
                                        )
        create_user_button.grid(row=8, column=1, padx=5,
                                pady=5, sticky=(constants.NS, constants.EW))

    def _initialize(self):
        self._initialize_frame()

        self._initialize_error()

        self._initialize_login_fields()

        self._hide_error()
