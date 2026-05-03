from tkinter import ttk, constants
from ui.view import ViewBase


class LoginView(ViewBase):
    """Luokka vastaa sovelluksen kirjautumisnäkymästä.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: käyttäjätoiminnoista vastaava olio
            _message_variable (StringVar): merkkijonomuuttuja, 
                joka säilyttää näytöllä näytettävää viestiä
            _message_label (Label): viestin näyttämisestä vastaava Label-olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
            _grid_size (tuple): monikko, 
                joka sisältää näkymän kehyksen ristikon rivien ja sarakkeiden määrän
            _create_user_view: käyttäjänluontinäkymä
            _front_view: sovelluksen etusivu kirjauduttua
            _username (Entry): Entry-olio, joka säilyttää käyttäjän antaman käyttäjätunnuksen
            _password (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan
            _header (HeaderFrame): näkymän yläviitekenttä
            _message (String): näkymässä näytettävä viesti
            _message_win (Toplevel): käyttöliittymän päälle luotava ikkuna viestejä varten
            _question_answer (bool): käyttäjän vastaus kysymysikkunan kysymykseeen
            _configs: käyttöliittymän ominaisuuksien arvot tiedostossa
    """

    def __init__(self, *, root, service, configs, header, views, message):
        """Luo kirjautumisnäkymä.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: käyttäjätoiminnoista vastaava olio
            configs: käyttöliittymän ominaisuuksien arvot tiedostossa
            header (HeaderFrame): näkymän yläviitekenttä
            views (dict): hajautustaulu, joka sisältää luokan käyttämiä näkymiä
                keys:
                    create_user_view: käyttäjänluontinäkymä
                    front_view: sevelluksen etusivu kirjauduttua
            message (String): näkymässä näytettävä viesti
        """
        self._create_user_view = views["create_user_view"]
        self._front_view = views["front_view"]
        self._username = None
        self._password = None
        if not message:
            message = "Tervetuloa!"
        super().__init__(
            root=root,
            service=service,
            header=header,
            message=message,
            configs=configs
        )

    def _login_handler(self):
        self._hide_error()
        self._hide_message()
        username = self._username.get()
        password = self._password.get()

        try:
            user = self._service.get_user_service().login(username, password)
            self._front_view(f"Tervetuloa {user.username}!")
        except self._service.get_user_service().get_exceptions().InvalidCredentials as e:
            self._show_error(e.message)

    def _initialize_login_fields(self):
        username_label = ttk.Label(
            master=self._frame,
            text="Käyttäjänimi:"
        )
        username_label.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )
        self._username = ttk.Entry(master=self._frame)
        self._username.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        password_label = ttk.Label(
            master=self._frame,
            text="Salasana:"
        )
        password_label.grid(
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )
        self._password = ttk.Entry(master=self._frame, show="*")
        self._password.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        login_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu",
            command=self._login_handler
        )
        login_button.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

    def _initialize_create_user(self):
        create_user_button = ttk.Button(
            master=self._frame,
            text="Rekisteröidy",
            command=self._create_user_view
        )
        create_user_button.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()
        self._header.configure(
            {"row": 0,
             "column": 0,
             "rowspan": 1,
             "columnspan": self._root.grid_size()[0]}
        )
        self._initialize_error()

        self._initialize_message()
        self._show_message(self._message)

        self._initialize_login_fields()
        self._initialize_create_user()

        self._hide_error()
