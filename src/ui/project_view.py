from tkinter import ttk, constants, scrolledtext as stext
from ui.session_view import SessionView


class ProjectView(SessionView):
    """Luokka vastaa hankenäkymästä.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: toiminnoista vastaava olio
            _message_variable (StringVar): merkkijonomuuttuja, joka säilyttää näytöllä näytettävää viestiä
            _message_label (Label): viestin näyttämisestä vastaava Label-olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
            _grid_size (tuple): monikko, joka sisältää näkymän kehyksen ristikon rivien ja sarakkeiden määrän
            _center_column (int): ristikon keskimmäinen ruutu
            _project (Project): näytettävä hanke
            _margins (dict): viitekentät hajautustaulussa:
                Keys:
                    header (HeaderFrame): näkymän yläviitekenttä 
                    footer (MarginFrame): näkymän alaviitekenttä
                    left_margin (MarginFrame): näkymän vasen viitekenttä
                    right_margin (MarginFrame): näkymän oikea viitekenttä
            _edit_project_view: metodi, vie hankkeen muokkausnäkymään
            _back_to_front_view: metodi, joka palauttaa etusivun
            _message (String): näkymässä näytettävä viesti
            _message_win (Toplevel): käyttöliittymän päälle luotava ikkuna viestejä varten
            _question_answer (bool): käyttäjän vastaus kysymysikkunan kysymykseeen
            _query (String): hakusana, jota käytettiin edellisen näkymän hakutulosten muodostamiseen, jos edellinen näkymä oli hakutulosnäkymä
            _page (int): hakutulosten sivunumero, joka näytettiin hakutulosnäkymässä
            _back_to_search_results: metodi, joka palauttaa hakutulokset
    """

    def __init__(self, root, service, margins, view_params, inputs):
        """Näytä hanke.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            margins (dict): viitekentät hajautustaulussa:
                Keys:
                    header (HeaderFrame): näkymän yläviitekenttä 
                    footer (MarginFrame): näkymän alaviitekenttä
                    left_margin (MarginFrame): näkymän vasen viitekenttä
                    right_margin (MarginFrame): näkymän oikea viitekenttä
            view_params (dict): hajautustaulu, joka sisältää näkymämetodeja
                Keys:
                    edit_project_view: metodi, vie hankkeen muokkausnäkymään
                    back_to_front_view: metodi, joka palauttaa etusivun
                    back_to_search_results: metodi, joka palauttaa hakutulokset
            inputs (dict): näkymälle dataa
                keys:
                    project (Project): näytettävä hanke
                    message (String): näkymässä näytettävä viesti
                    query (String): hakusana, jota käytettiin edellisen näkymän hakutulosten muodostamiseen, jos edellinen näkymä oli hakutulosnäkymä
                    page (int): hakutulosten sivunumero, joka näytettiin hakutulosnäkymässä
        """
        super().__init__(root=root, service=service,
                         margins=margins, message=inputs["message"])
        self._project = inputs["project"]
        self._edit_project_view = view_params["edit_project_view"]
        self._back_to_front_view = view_params["back_to_front_view"]
        self._back_to_search_results = view_params["back_to_search_results"]
        self._query = inputs["query"]
        self._page = inputs["page"]

    def _edit_project_handler(self):
        self._edit_project_view(
            message=None, project=self._project, query=self._query, page=self._page)

    def _remove_project_handler(self):
        self._question_window(
            title="Poista maailma",
            message="Haluatko poistaa maailman pysyvästi?",
            yes_text="Kyllä",
            no_text="En"
        )

    def _question_answer_handler(self):
        if self._question_answer:
            try:
                user = self._service.get_user_service().get_current_user()
                self._service.get_project_service().remove_project(user, self._project)
                if self._query:
                    message = "Maailman poistaminen onnistui."
                    self._back_to_search_results(
                        message=message, query=self._query, page=self._page)
                else:
                    self._back_to_front_view(
                        message="Maailman poistaminen onnistui.")
            except self._service.get_project_service().get_exceptions().UserNotOwnerOfProject as e:
                self._show_error(e.message)

    def _back_to_search_handler(self):
        self._back_to_search_results(
            message=None, query=self._query, page=self._page)

    def _initialize_project_fields(self):
        name_label = ttk.Label(
            master=self._frame,
            text=self._project.title
        )
        name_label.grid(
            column=self._grid_size[0]//2,
            row=1,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )

        class_label = ttk.Label(
            master=self._frame,
            text="Luokka:"
        )
        class_label.grid(
            column=self._grid_size[0]//2-1,
            row=2,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.E)
        )

        project_class = ttk.Label(
            master=self._frame,
            text=self._project.p_type.value
        )
        project_class.grid(
            column=self._grid_size[0]//2,
            row=2,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        description_label = ttk.Label(
            master=self._frame,
            text="Kuvaus:"
        )
        description_label.grid(
            column=self._grid_size[0]//2-1,
            row=3,
            padx=5,
            pady=5,
            sticky=(constants.N, constants.E)
        )

        description_text = stext.ScrolledText(master=self._frame)
        description_text.insert(constants.END, self._project.description)
        description_text.configure(state='disabled')
        description_text.grid(
            column=self._grid_size[0]//2,
            row=3,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        owner_label = ttk.Label(
            master=self._frame,
            text="Haltija:"
        )
        owner_label.grid(
            column=self._grid_size[0]//2-1,
            row=4,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.E)
        )

        owner = ttk.Label(
            master=self._frame,
            text=self._project.owner.username
        )
        owner.grid(
            column=self._grid_size[0]//2,
            row=4,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        edit_button = ttk.Button(
            master=self._frame,
            text="Muokkaa",
            command=self._edit_project_handler
        )
        edit_button.grid(
            column=self._grid_size[0]//2,
            row=5,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        remove_button = ttk.Button(
            master=self._frame,
            text="Poista",
            command=self._remove_project_handler
        )
        remove_button.grid(
            column=self._grid_size[0]//2+1,
            row=5,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

    def _initialize_back_to_search_results(self):
        results_button = ttk.Button(
            master=self._frame,
            text="Takaisin hakutuloksiin",
            command=self._back_to_search_handler
        )
        results_button.grid(
            column=self._grid_size[0]//2,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_rowconfigure(4, weight=1)
        self._frame.grid_rowconfigure(5, weight=1)
        self._frame.grid_rowconfigure(6, weight=1)

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)

        self._grid_size = self._frame.grid_size()

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()

        try:
            self._service.get_user_service().get_current_user()
            self._margins["header"].configure(
                {"row": 0,
                 "column": 0,
                 "rowspan": 2,
                 "columnspan": self._root.grid_size()[0]}
            )
            self._initialize_error()
            self._initialize_project_fields()
            if self._query:
                self._initialize_back_to_search_results()
        except self._service.get_user_service().get_exceptions().SessionNotFound as e:
            self._initialize_error()
            self._show_error(e.message)

        self._hide_error()
