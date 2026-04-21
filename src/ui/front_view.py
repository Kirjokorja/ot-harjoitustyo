from tkinter import ttk, constants
from ui.session_view import SessionView


class FrontView(SessionView):
    """Luokka vastaa sovelluksen etusivusta käyttäjän kirjauduttua.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: toiminnoista vastaava olio
            _new_project: uuden hankkeen luomisnäkymä
            _back_to_front_view: metodi, joka paluttaa käyttäjän etusivun
            _back_to_login: metodi, joka palauttaa kirjautumisnäkymän
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksen näyttämisestä vastaava Label-olio
            _header (Header): yläviitekenttä
            _footer (Footer): alaviitekenttä
            _margin_left (MarginLeft): vasen viitekenttä
            _margin_right (MarginRight): oikea viitekenttä
    """

    def __init__(self, root, service, margins):
        """Luo kirjautuneen etusivu.

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

            greeting = ttk.Label(
                master=self._frame,
                text=f"Tervetuloa {user.username}!",
                anchor="center"
            )

            greeting.grid(
                padx=5,
                pady=5,
                columnspan=self._grid_size[0],
                sticky=(constants.NS, constants.EW)
            )
        except self._service.get_user_service().get_exceptions().SessionNotFound as e:
            self._initialize_error()
            self._show_error(e.message)

        self._hide_error()
