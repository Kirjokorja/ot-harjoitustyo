from tkinter import ttk, constants
from ui.session_view import SessionView


class FrontView(SessionView):
    """Luokka vastaa sovelluksen etusivusta käyttäjän kirjauduttua.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: toiminnoista vastaava olio
            _message_variable (StringVar): merkkijonomuuttuja, joka säilyttää näytöllä näytettävää viestiä
            _message_label (Label): viestin näyttämisestä vastaava Label-olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
            _grid_size (tuple): monikko, joka sisältää näkymän kehyksen ristikon rivien ja sarakkeiden määrän
            _new_project: uuden hankkeen luomisnäkymä
            _back_to_front_view: metodi, joka paluttaa käyttäjän etusivun
            _back_to_login: metodi, joka palauttaa kirjautumisnäkymän
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksen näyttämisestä vastaava Label-olio
            _margins (dict): viitekentät hajautustaulussa:
                keys:
                    header (HeaderFrame): näkymän yläviitekenttä 
                    footer (MarginFrame): näkymän alaviitekenttä
                    left_margin (MarginFrame): näkymän vasen viitekenttä
                    right_margin (MarginFrame): näkymän oikea viitekenttä
            _message (String): näkymässä näytettävä viesti
            _message_win (Toplevel): käyttöliittymän päälle luotava ikkuna viestejä varten
            _question_answer (bool): käyttäjän vastaus kysymysikkunan kysymykseeen
    """

    def __init__(self, root, service, margins, message):
        """Luo kirjautuneen etusivu.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            margins (dict): viitekentät hajautustaulussa:
                keys:
                    header (HeaderFrame): näkymän yläviitekenttä 
                    footer (MarginFrame): näkymän alaviitekenttä
                    left_margin (MarginFrame): näkymän vasen viitekenttä
                    right_margin (MarginFrame): näkymän oikea viitekenttä
            message (String): näkymässä näytettävä viesti
        """
        super().__init__(root=root, service=service, margins=margins, message=message)

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()

        try:
            user = self._service.get_user_service().get_current_user()
            self._margins["header"].configure(
                {"row": 0,
                 "column": 0,
                 "rowspan": 2,
                 "columnspan": self._root.grid_size()[0]}
            )
            self._initialize_error()

            self._initialize_message()
            self._show_message(self._message)
        except self._service.get_user_service().get_exceptions().SessionNotFound as e:
            self._initialize_error()
            self._show_error(e.message)

        self._hide_error()
