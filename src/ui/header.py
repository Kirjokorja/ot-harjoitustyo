from tkinter import ttk, constants
from ui.margin import MarginFrame


class HeaderFrame(MarginFrame):
    """Luokka kuvaa yläviitekenttäkehystä.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätään
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _row (int): rivi, jolle kehys sijoitetaan ikkunassa
            _column (int): sarake, johon kehys sijoitetaan ikkunassa
            _rowspan (int): kehyksen korkeus ikkunassa 
            _columnspan (int): kehyksen leveys ikkunassa
            _service: toiminnoista vastaava olio
            _search_field (Entry): Entry-olio,
                joka ottaa vastaan ja säilyttää käyttäjän antaman hakusanan
            _back_to_front_view: metodi, joka palauttaa alkunäkymän
            _back_to_login_view: metodi, joka palauttaa kirjautumisnäkymän
            _new_project_view: metodi, joka vie hankkeen luomisnäkymään
            _search_results_view: metodi, joka näyttää haun tulokset
    """

    def __init__(
        self,
        root,
        service,
        views
    ):
        """Luo ylväviitekenttä.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            views (dict): hajautustaulu, joka sisältää tarvittavat näkymämetodit
                keys:
                    back_to_front_view: metodi, joka palauttaa alkunäkymän
                    back_to_login_view: metodi, joka palauttaa kirjautumisnäkymän
                    new_project_view: metodi, joka vie hankkeen luomisnäkymään
                    search_results_view: metodi, joka näyttää haun tulokset
        """
        self._service = service
        self._back_to_front_view = views["back_to_front_view"]
        self._back_to_login_view = views["back_to_login_view"]
        self._new_project_view = views["new_project_view"]
        self._search_results_view = views["search_results_view"]
        self._search_field = None

        super().__init__(root=root)

    def _logout_handler(self):
        self._service.get_user_service().logout()
        self._back_to_login_view()

    def _search_handler(self):
        self._search_results_view(message=None, query=self._search_field.get())

    def _initialize_info(self, user, info_frame):
        user_label = ttk.Label(
            master=info_frame,
            text=f"Olet kirjautunut sisään nimellä {user.username}."
        )
        user_label.grid(
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )
        user_label.grid_columnconfigure(0, weight=3)

    def _initialize_nav_buttons(self, user, nav_frame):
        style = ttk.Style()
        style.configure("SmallFrame.TFrame", foreground="black",
                        background="blue")
        nav_frame.configure(style="SmallFrame.TFrame")

        front_view_button = ttk.Button(
            master=nav_frame,
            text="Etusivu",
            command=self._back_to_front_view,
        )
        front_view_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )
        nav_frame.grid_columnconfigure(0, weight=2)

        if user:
            new_project_button = ttk.Button(
                master=nav_frame,
                text="Luo maailma",
                command=self._new_project_view
            )
            new_project_button.grid(
                row=0,
                column=1,
                padx=5,
                pady=5,
                sticky=(constants.NS, constants.W)
            )
            nav_frame.grid_columnconfigure(1, weight=2)

            logout_button = ttk.Button(
                master=nav_frame,
                text="Kirjaudu ulos",
                command=self._logout_handler
            )
            logout_button.grid(
                row=0,
                column=2,
                padx=5,
                pady=5,
                sticky=(constants.NS, constants.W)
            )
            nav_frame.grid_columnconfigure(2, weight=2)

    def _initialize_search_field(self, search_frame):
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=10)
        search_frame.grid_columnconfigure(2, weight=1)

        search_label = ttk.Label(
            master=search_frame,
            text="Haku:"
        )
        search_label.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )
        self._search_field = ttk.Entry(master=search_frame)
        self._search_field.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )
        search_button = ttk.Button(
            master=search_frame,
            text="Hae",
            command=self._search_handler
        )
        search_button.grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

    def _initialize_header(self, user):
        if user:
            info_frame = ttk.Frame(master=self._frame)
            self._initialize_info(user=user, info_frame=info_frame)
            info_frame.grid(
                columnspan=self._columnspan,
                sticky=constants.EW
            )

        nav_frame = ttk.Frame(master=self._frame)
        self._initialize_nav_buttons(user=user, nav_frame=nav_frame)
        nav_frame.grid(
            columnspan=self._columnspan//2,
            sticky=constants.EW
        )
        if user:
            search_frame = ttk.Frame(master=self._frame)
            self._initialize_search_field(search_frame=search_frame)
            search_frame.grid(
                columnspan=self._columnspan//4,
                sticky=constants.EW
            )

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        style = ttk.Style()
        style.configure("Header.TFrame", foreground="black",
                        background="green")

        self._frame.configure(style="Header.TFrame")

        for i in range(self._rowspan):
            self._frame.grid_rowconfigure(i, weight=1)

        for i in range(self._columnspan):
            self._frame.grid_columnconfigure(i, weight=1)

    def _initialize(self):
        self._initialize_frame()
        user = None
        try:
            user = self._service.get_user_service().get_current_user()
        except self._service.get_user_service().get_exceptions().SessionNotFound:
            self._back_to_front_view = self._back_to_login_view

        self._initialize_header(user)
