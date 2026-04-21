from tkinter import ttk
from ui.view import ViewBase


class SessionView(ViewBase):
    """Luokka kuvaa käyttöliittymänäkymää istunnon aikana.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätään
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: toiminnoista vastaava olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
            _grid_size (tuple): monikko, joka sisältää näkymän kehyksen ristikon rivien ja sarakkeiden määrän
            _center_column (int): ristikon keskimmäinen ruutu
            _header (Header): yläviitekenttä
            _footer (Footer): alaviitekenttä
            _margin_left (MarginLeft): vasen viitekenttä
            _margin_right (MarginRight): oikea viitekenttä
            _back_to_front_view: metodi, joka paluttaa käyttäjän etusivun
            _back_to_login: metodi, joka palauttaa kirjautumisnäkymän
            _new_project: hankkeen luomisnäkymä
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksen näyttämisestä vastaava Label-olio
    """

    def __init__(self, root, service, margins):
        """Luo kirjautuneen näkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            margins (dict): viitekentät hajautustaulussa:
                header (HeaderFrame): näkymän yläviitekenttä 
                footer (MarginFrame): näkymän alaviitekenttä
                left_margin (MarginFrame): näkymän vasen viitekenttä
                right_margin (MarginFrame): näkymän oikea viitekenttä
        """
        super().__init__(root=root, service=service, margins=margins)

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)

        self._grid_size = self._frame.grid_size()

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()

        try:
            user = self._service.get_user_service().get_current_user()
            self._header.configure(
                {"row": 0,
                 "column": 0,
                 "rowspan": 2,
                 "columnspan": self._root.grid_size()[0]}
            )
            self._initialize_error()
        except self._service.get_user_service().get_exceptions().SessionNotFound as e:
            self._initialize_error()
            self._show_error(e.message)

        self._hide_error()
