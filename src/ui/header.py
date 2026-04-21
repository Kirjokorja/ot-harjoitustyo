from tkinter import ttk, constants
from ui.margin import MarginFrame


class HeaderFrame(MarginFrame):
    """Luokka kuvaa yläviitekenttäkehystä.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätään
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _row (int): rivi, jolle kehys sijoitetaan ikkunassa
            _column (int): sarake, johon kehys sijoitetaan ikkunassa
            _rowspan (int): kehyksen korkeus ikkunassa 
            _columnspan (int): kehyksen leveys ikkunassa
            _service: toiminnoista vastaava olio
            _back_to_front_view: metodi, joka palauttaa alkunäkymän
            _back_to_login_view: metodi, joka palauttaa kirjautumisnäkymän
            _new_project_view: metodi, joka vie hankkeen luomisnäkymään
    """

    def __init__(
        self,
        root,
        service,
        back_to_front_view,
        back_to_login_view,
        new_project_view
    ):
        """Luo ylväviitekenttä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            back_to_front_view: metodi, joka palauttaa alkunäkymän
            back_to_login_view: metodi, joka palauttaa kirjautumisnäkymän
            new_project_view: metodi, joka vie hankkeen luomisnäkymään
        """
        self._service = service
        self._back_to_front_view = back_to_front_view
        self._back_to_login_view = back_to_login_view
        self._new_project_view = new_project_view

        super().__init__(root=root)

    def _logout_handler(self):
        self._service.get_user_service().logout()
        self._back_to_login_view()

    def _initialize_header(self, user=None):

        user_label = ttk.Label(
            master=self._frame,
            text=f"Olet kirjautunut sisään nimellä {user.username}."
        )
        user_label.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            columnspan=self._columnspan,
            sticky=constants.W
        )

        new_project_button = ttk.Button(
            master=self._frame,
            text="Luo maailma",
            command=self._new_project_view
        )
        new_project_button.grid(
            row=self._rowspan-1,
            column=1,
            padx=5,
            pady=10,
            sticky=constants.W
        )

        logout_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu ulos",
            command=self._logout_handler
        )
        logout_button.grid(
            row=self._rowspan-1,
            column=2,
            padx=5,
            pady=10,
            sticky=constants.W
        )

    def _initialize_back_to_start(self):

        front_view_button = ttk.Button(
            master=self._frame,
            text="Etusivu",
            command=self._back_to_front_view
        )
        front_view_button.grid(
            row=self._rowspan-1,
            column=0,
            padx=10,
            pady=10,
            sticky=constants.W
        )

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        style = ttk.Style()
        style.configure("Header.TFrame", foreground="black", background="green")

        self._frame.configure(style="Header.TFrame")

        for i in range(self._rowspan):
            self._frame.grid_rowconfigure(i, weight=1)

        for i in range(self._columnspan):
            self._frame.grid_columnconfigure(i, weight=1)

    def _initialize(self):
        self._initialize_frame()
        try:
            user=self._service.get_user_service().get_current_user()
            self._initialize_header(user)
        except self._service.get_user_service().get_exceptions().SessionNotFound:
            self._back_to_front_view = self._back_to_login_view
        self._initialize_back_to_start()
