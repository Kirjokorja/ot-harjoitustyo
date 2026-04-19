from tkinter import ttk, constants, StringVar, scrolledtext as stext, END


class ProjectView:
    """Luokka vastaa hankenäkymästä.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _services: toiminnoista vastaava olio
            _project (Project): näytettävä hanke
            _back_to_front_view: metodi, joka paluttaa käyttäjän etusivun
            _back_to_login: metodi, joka palauttaa kirjautumisnäkymän
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksen näyttämisestä vastaava Label-olio
            _user (User): istunnon haltijan käyttäjäolio
    """

    def __init__(self, root, services, project, back_to_front_view, back_to_login):
        """Näytä hanke.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            services: toiminnoista vastaava olio
            project (Project): näytettävä hanke
            back_to_front_view: metodi, joka paluttaa käyttäjän etusivun
            back_to_login: metodi, joka palauttaa kirjautumisnäkymän
        """
        self._root = root
        self._services = services
        self._project = project
        self._back_to_front_view = back_to_front_view
        self._back_to_login = back_to_login
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

    def _initialize_project_fields(self):
        name_label = ttk.Label(
            master=self._frame,
            text=self._project.title
        )
        name_label.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

        class_label = ttk.Label(
            master=self._frame,
            text="Luokka:"
        )
        class_label.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

        project_class = ttk.Label(
            master=self._frame,
            text=self._project.p_type.value
        )
        project_class.grid(
            row=4,
            column=2,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        description_label = ttk.Label(
            master=self._frame,
            text="Kuvaus:"
        )
        description_label.grid(
            row=5,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

        description = stext.ScrolledText(master=self._frame)
        description.insert(END, self._project.description)
        description.grid(
            row=5,
            column=2,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        owner_label = ttk.Label(
            master=self._frame,
            text="Haltija:"
        )
        owner_label.grid(
            row=6,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

        owner = ttk.Label(
            master=self._frame,
            text=self._project.owner.username
        )
        owner.grid(
            row=6,
            column=2,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
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
