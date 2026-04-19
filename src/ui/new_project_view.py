from tkinter import ttk, constants, StringVar, scrolledtext as stext, END


class NewProjectView:
    """Luokka vastaa uuden hankkeen luomisnäkymästä.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _services: toiminnoista vastaava olio
            _back_to_front_view: metodi, joka paluttaa käyttäjän etusivun
            _back_to_login: metodi, joka palauttaa kirjautumisnäkymän
            _project_view: hankenäkymä
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksen näyttämisestä vastaava Label-olio
            _user (User): istunnon haltijan käyttäjäolio
            _project_name (Entry): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen nimen
            _project_class (Combobox): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen luokan
            _project_description (ScrolledText): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen kuvauksen
            _classes (list<TypeClass>): hankeen luokat
    """

    def __init__(self, root, services, back_to_front_view, back_to_login, project_view):
        """Luo hankkeenluontinäkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            services: toiminnoista vastaava olio
            back_to_front_view: metodi, joka paluttaa käyttäjän etusivun
            back_to_login: metodi, joka palauttaa kirjautumisnäkymän
            project_view: hankenäkymä
        """
        self._root = root
        self._services = services
        self._back_to_front_view = back_to_front_view
        self._back_to_login = back_to_login
        self._project_view = project_view
        self._frame = None
        self._error_variable = None
        self._error_label = None
        self._user = None
        self._project_name = None
        self._project_class = None
        self._project_description = None
        self._classes = self._services.get_project_service().get_project_classes("Hanke")

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

        front_view_button = ttk.Button(
            master=self._frame,
            text="Etusivu",
            command=self._back_to_front_view
        )
        front_view_button.grid(
            padx=10,
            pady=10,
            sticky=constants.EW
        )

        logout_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu ulos",
            command=self._logout_handler
        )
        logout_button.grid(
            padx=10,
            pady=10,
            sticky=constants.EW
        )

    def _get_class_object(self):
        for type_class in self._classes:
            if type_class.value == self._project_class.get():
                return type_class
        return None

    def _create_project_handler(self):
        self._hide_error()
        try:
            project = self._services.get_project_service().create_project(
                self._project_name.get(),
                self._get_class_object(),
                self._project_description.get("1.0", END),
                self._user
            )
            self._project_view(project)
        except (self._services.get_project_service().get_exceptions().ProjectHasNoTitle,
                self._services.get_project_service().get_exceptions().ProjectHasNoType,
                self._services.get_project_service().get_exceptions().ProjectHasNoOwner) as e:
            self._show_error(e.message)

    def _initialize_project_fields(self):
        name_label = ttk.Label(
            master=self._frame,
            text="Nimi*:"
        )
        name_label.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

        self._project_name = ttk.Entry(master=self._frame)
        self._project_name.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        class_label = ttk.Label(
            master=self._frame,
            text="Luokka*:"
        )
        class_label.grid(
            row=5,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

        self._project_class = ttk.Combobox(
            master=self._frame,
            values=[type.value for type in self._classes]
        )
        self._project_class.set("Valitse luokka.")
        self._project_class.grid(
            row=6,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        description_label = ttk.Label(
            master=self._frame,
            text="Kuvaus:"
        )
        description_label.grid(
            row=7,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

        self._project_description = stext.ScrolledText(master=self._frame)
        self._project_description.grid(
            row=8,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        create_button = ttk.Button(
            master=self._frame,
            text="Luo",
            command=self._create_project_handler
        )
        create_button.grid(
            row=9,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        name_label = ttk.Label(
            master=self._frame,
            text="*Pakolliset tiedot"
        )
        name_label.grid(
            row=10,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_error()

        try:
            self._user = self._services.get_user_service().get_current_user()
            self._initialize_header()
            self._initialize_project_fields()
        except self._services.get_user_service().get_exceptions().NoSessionFound as e:
            self._show_error(e.message)

        self._hide_error()
