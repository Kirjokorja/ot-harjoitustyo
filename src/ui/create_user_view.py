from tkinter import ttk, constants
from ui.view import ViewBase


class CreateUserView(ViewBase):
    """Luokka vastaa sovelluksen käyttäjänluontinäkymästä.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: käyttäjätoiminnoista vastaava olio
            _message_variable (StringVar): merkkijonomuuttuja, joka säilyttää näytöllä näytettävää viestiä
            _message_label (Label): viestin näyttämisestä vastaava Label-olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
            _grid_size (tuple): monikko, joka sisältää näkymän kehyksen ristikon rivien ja sarakkeiden määrän
            _center_column (int): ristikon keskimmäinen ruutu
            _margins (dict): viitekentät hajautustaulussa:
                keys:
                    header (HeaderFrame): näkymän yläviitekenttä 
                    footer (MarginFrame): näkymän alaviitekenttä
                    left_margin (MarginFrame): näkymän vasen viitekenttä
                    right_margin (MarginFrame): näkymän oikea viitekenttä
            _back_to_start_view: metodi, joka palauttaa alkunäkymän
            _username (Entry): Entry-olio, joka säilyttää käyttäjän antaman käyttäjätunnuksen
            _password (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan 
            _password_confirm (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan tarkistusta varten
            _message (String): näkymässä näytettävä viesti
            _message_win (Toplevel): käyttöliittymän päälle luotava ikkuna viestejä varten
            _question_answer (bool): käyttäjän vastaus kysymysikkunan kysymykseeen
            _configs: käyttöliittymän ominaisuuksien arvot tiedostossa
    """

    def __init__(self, *, root, service, configs, header, back_to_start_view, message):
        """Luo käyttäjänluontinäkymä.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: käyttäjätoiminnoista vastaava olio
            configs: käyttöliittymän ominaisuuksien arvot tiedostossa
            header (HeaderFrame): näkymän yläviitekenttä 
            back_to_start_view: metodi, joka palauttaa alkunäkymän
            message (String): näkymässä näytettävä viesti
        """
        self._username = None
        self._password = None
        self._password_confirm = None
        self._back_to_start_view = back_to_start_view
        super().__init__(
            root=root,
            service=service,
            header=header,
            message=message,
            configs=configs
        )

    def _create_user_handler(self):
        self._hide_error()
        username = self._username.get()
        password = self._password.get()
        password_confirm = self._password_confirm.get()

        try:
            user = self._service.get_user_service().create_user(
                username, password, password_confirm)
            self._back_to_start_view(
                f"Käyttäjä {user.username} on luotu onnistuneesti.")
        except (self._service.get_user_service().get_exceptions().UserAlreadyExists,
                self._service.get_user_service().get_exceptions().UsernameTooShort,
                self._service.get_user_service().get_exceptions().PasswordTooShort,
                self._service.get_user_service().get_exceptions().PasswordsDoNotMatch) as e:
            self._show_error(e.message)

    def _initialize_create_fields(self):
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
            text=f"Salasana (min {self._service.get_user_service().get_min_password_lenght()} merkkiä):"
        )
        password_label.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )
        self._password = ttk.Entry(master=self._frame, show="*")
        self._password.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        password_confirm_label = ttk.Label(
            master=self._frame,
            text="Salasana uudestaan:"
        )
        password_confirm_label.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )
        self._password_confirm = ttk.Entry(master=self._frame, show="*")
        self._password_confirm.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        create_user_button = ttk.Button(
            master=self._frame,
            text="Luo",
            command=self._create_user_handler
        )
        create_user_button.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

    def initialize(self):
        self._initialize_frame()
        self._header.configure(
            {"row": 0,
             "column": 0,
             "rowspan": 1,
             "columnspan": self._root.grid_size()[0]}
        )
        self._initialize_error()
        self._initialize_create_fields()

        self._hide_error()
