from tkinter import ttk, constants, scrolledtext as stext
from ui.session_view import SessionView


class EditProjectView(SessionView):
    """Luokka vastaa uuden hankkeen muokkausnäkymästä.

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
            _margins (dict): viitekentät hajautustaulussa:
                keys:
                    header (HeaderFrame): näkymän yläviitekenttä 
                    footer (MarginFrame): näkymän alaviitekenttä
                    left_margin (MarginFrame): näkymän vasen viitekenttä
                    right_margin (MarginFrame): näkymän oikea viitekenttä
            _project_view: hankenäkymä
            _project_name (Entry): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen nimen
            _project_class (Combobox): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen luokan
            _project_description (ScrolledText): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen kuvauksen
            _project (Project): hankeolio
            _classes (list<TypeClass>): hankeen luokat
            _message (String): näkymässä näytettävä viesti
            _message_win (Toplevel): käyttöliittymän päälle luotava ikkuna viestejä varten
            _question_answer (bool): käyttäjän vastaus kysymysikkunan kysymykseeen
            _query (String): hakusana, jota käytettiin hankkeen löytämiseen
            _page (int): hakutulosten sivunumero, josta hanke löydettin
    """

    def __init__(self, root, service, margins, project_view, inputs):
        """Luo hankkeenmuokkausnäkymä.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            margins (dict): viitekentät hajautustaulussa:
                keys:
                    header (HeaderFrame): näkymän yläviitekenttä 
                    footer (MarginFrame): näkymän alaviitekenttä
                    left_margin (MarginFrame): näkymän vasen viitekenttä
                    right_margin (MarginFrame): näkymän oikea viitekenttä
            inputs (dict): näkymälle dataa
                keys:
                    project (Project): näytettävä hanke
                    message (String): näkymässä näytettävä viesti
                    query (String): hakusana, jota käytettiin hankkeen löytämiseen
                    page (int): hakutulosten sivunumero, josta hanke löydettin
        """
        self._project_view = project_view
        self._project_name = None
        self._project_class = None
        self._project_description = None
        self._project = inputs["project"]
        self._query = inputs["query"]
        self._page = inputs["page"]
        super().__init__(root=root, service=service,
                         margins=margins, message=inputs["message"])
        self._classes = self._service.get_project_service().get_project_classes()

    def _get_class_object(self):
        for type_class in self._classes:
            if type_class.value == self._project_class.get():
                return type_class
        return None

    def _save_show_project_handler(self):
        self._hide_error()
        self._hide_message()
        try:
            self._project.title = self._project_name.get()
            self._project.p_type = self._get_class_object()
            self._project.description = self._project_description.get(
                "1.0", constants.END)
            self._project = self._service.get_project_service().save_project(self._project)
            self._project_view(message=None, project=self._project,
                               query=self._query, page=self._page)
        except (self._service.get_project_service().get_exceptions().ProjectHasNoTitle,
                self._service.get_project_service().get_exceptions().ProjectHasNoType,
                self._service.get_project_service().get_exceptions().ProjectHasNoOwner) as e:
            self._show_error(e.message)

    def _save_project_handler(self):
        self._hide_error()
        self._hide_message()
        try:
            self._project.title = self._project_name.get()
            self._project.p_type = self._get_class_object()
            self._project.description = self._project_description.get(
                "1.0", constants.END)
            self._project = self._service.get_project_service().save_project(self._project)
            self._show_message("Maailma tallennettu.")
        except (self._service.get_project_service().get_exceptions().ProjectHasNoTitle,
                self._service.get_project_service().get_exceptions().ProjectHasNoType,
                self._service.get_project_service().get_exceptions().ProjectHasNoOwner) as e:
            self._show_error(e.message)

    def _back_to_project_handler(self):
        self._project_view(message=None, project=self._project,
                           query=self._query, page=self._page)

    def _initialize_project_fields(self):
        name_label = ttk.Label(
            master=self._frame,
            text="Nimi*:"
        )
        name_label.grid(
            row=1,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )

        self._project_name = ttk.Entry(master=self._frame)
        self._project_name.insert(0, self._project.title)
        self._project_name.grid(
            row=2,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        class_label = ttk.Label(
            master=self._frame,
            text="Luokka*:"
        )
        class_label.grid(
            row=3,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )

        self._project_class = ttk.Combobox(
            master=self._frame,
            values=[type.value for type in self._classes],
            state="readonly"
        )
        self._project_class.set(self._project.p_type.value)
        self._project_class.grid(
            row=4,
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
            row=5,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )

        self._project_description = stext.ScrolledText(master=self._frame)
        self._project_description.insert(
            constants.END, self._project.description)
        self._project_description.grid(
            row=6,
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        create_button = ttk.Button(
            master=self._frame,
            text="Tallenna ja näytä",
            command=self._save_show_project_handler
        )
        create_button.grid(
            row=7,
            column=self._grid_size[0]//2-1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        save_button = ttk.Button(
            master=self._frame,
            text="Tallenna",
            command=self._save_project_handler
        )
        save_button.grid(
            row=7,
            column=self._grid_size[0]//2,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        save_button = ttk.Button(
            master=self._frame,
            text="Takaisin maailmaan",
            command=self._back_to_project_handler
        )
        save_button.grid(
            row=7,
            column=self._grid_size[0]//2+1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

        name_label = ttk.Label(
            master=self._frame,
            text="*Pakolliset tiedot"
        )
        name_label.grid(
            row=8,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.grid_rowconfigure(0, weight=0)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_rowconfigure(4, weight=1)
        self._frame.grid_rowconfigure(5, weight=1)
        self._frame.grid_rowconfigure(6, weight=1)
        self._frame.grid_rowconfigure(7, weight=1)
        self._frame.grid_rowconfigure(8, weight=1)

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
            self._initialize_message()
            self._initialize_error()
            self._initialize_project_fields()
        except self._service.get_user_service().get_exceptions().SessionNotFound as e:
            self._initialize_error()
            self._show_error(e.message)

        self._hide_error()
        self._hide_message()
