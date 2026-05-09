from ui.view import ViewBase


class FrontView(ViewBase):
    """Luokka vastaa sovelluksen etusivusta käyttäjän kirjauduttua.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätään
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: toiminnoista vastaava olio
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
            _message (String): näkymässä näytettävä viesti
            _message_win (Toplevel): käyttöliittymän päälle luotava ikkuna viestejä varten
            _question_answer (bool): käyttäjän vastaus kysymysikkunan kysymykseeen
            _config: käyttöliittymän ominaisuuksien arvot tiedostossa
    """

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()

        if not self._message:
            self._message = self._config.FRONT_PAGE_GREET

        try:
            self._service.get_user_service().get_current_user()
            self._header.configure(
                {"row": 0,
                 "column": 0,
                 "rowspan": 3,
                 "columnspan": self._root.grid_size()[0]}
            )
            self._initialize_error()
            self._initialize_message()
            self._show_message(self._message)
        except self._service.get_user_service().get_exceptions().SessionNotFound as e:
            self._initialize_error()
            self._show_error(e.message)

        self._hide_error()
