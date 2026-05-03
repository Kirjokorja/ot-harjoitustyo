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
            _nav_button_1_logged_in: metodi, 
                joka ajetaan käyttäjän painaessa suunnistuspalkin ensimmäistä nappia 
                ollessaan kirjautuneena sisään
            _nav_button_1_logged_out: metodi, 
                joka ajetaan käyttäjän painaessa suunnistuspalkin ensimmäistä nappia 
                ollessaan kirjautuneena ulos
            _nav_button_2: metodi, joka ajetaan käyttäjän painaessa suunnistuspalkin toista nappia
            _nav_button_3: metodi, joka ajetaan käyttäjän painaessa suunnistuspalkin kolmatta nappia
            _search_results_view: metodi, joka näyttää haun tulokset
            _configs: käyttöliittymän ominaisuuksien arvot tiedostossa
    """

    def __init__(self, *, root, service, configs, buttons, search_results_view):
        """Luo ylväviitekenttä.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            configs: käyttöliittymän ominaisuuksien arvot tiedostossa
            buttons (dict): hajautustaulu, joka sisältääsuunnistuspalkin nappuloiden metodit
                keys:
                    nav_button_1_logged_in: metodi, 
                        joka ajetaan käyttäjän painaessa suunnistuspalkin ensimmäistä nappia
                        ollessaan kirjautuneena sisään
                    nav_button_1_logged_out: metodi, 
                        joka ajetaan käyttäjän painaessa suunnistuspalkin ensimmäistä nappia
                        ollessaan kirjautuneena ulos
                    nav_button_2: metodi, 
                        joka ajetaan käyttäjän painaessa suunnistuspalkin toista nappia
                    nav_button_3: metodi, 
                        joka ajetaan käyttäjän painaessa suunnistuspalkin kolmatta nappia
            search_results_view: metodi, joka näyttää haun tulokset
        """
        self._service = service
        self._nav_button_1_logged_in = buttons["nav_button_1_logged_in"]
        self._nav_button_1_logged_out = buttons["nav_button_1_logged_out"]
        self._nav_button_2 = buttons["nav_button_2"]
        self._nav_button_3 = buttons["nav_button_3"]
        self._search_results_view = search_results_view
        self._search_field = None

        super().__init__(root=root, configs=configs)

    def _search_handler(self):
        self._search_results_view(
            message=None,
            query=self._search_field.get(),
            page=1
        )

    def _initialize_info(self, user, info_frame):
        user_label = ttk.Label(
            master=info_frame,
            text=f"{self._configs.HEADER_INFO_MSG} {user.username}."
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

        nav_button_1_logged_in = ttk.Button(
            master=nav_frame,
            text=self._configs.HEADER_NAV_BUTTON_1,
            command=self._nav_button_1_logged_in,
        )
        nav_button_1_logged_in.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )
        nav_frame.grid_columnconfigure(0, weight=2)

        if user:
            nav_button_2 = ttk.Button(
                master=nav_frame,
                text=self._configs.HEADER_NAV_BUTTON_2,
                command=self._nav_button_2
            )
            nav_button_2.grid(
                row=0,
                column=1,
                padx=5,
                pady=5,
                sticky=(constants.NS, constants.W)
            )
            nav_frame.grid_columnconfigure(1, weight=2)

            nav_button_3 = ttk.Button(
                master=nav_frame,
                text=self._configs.HEADER_NAV_BUTTON_3,
                command=self._nav_button_3
            )
            nav_button_3.grid(
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
            text=self._configs.HEADER_SEARCH_LABEL
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
            text=self._configs.HEADER_SEARCH_BUTTON,
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
            self._nav_button_1_logged_in = self._nav_button_1_logged_out

        self._initialize_header(user)
