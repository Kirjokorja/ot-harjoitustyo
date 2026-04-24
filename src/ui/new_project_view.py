from tkinter import ttk, constants, scrolledtext as stext, END
from ui.session_view import SessionView


class NewProjectView(SessionView):
    """Luokka vastaa uuden hankkeen luomisnäkymästä.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
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
            _project_view: hankenäkymä
            _project_name (Entry): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen nimen
            _project_class (Combobox): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen luokan
            _project_description (ScrolledText): Tkinter-osanen, joka säilyttää käyttäjän syöttämän hankkeen kuvauksen
            _classes (list<TypeClass>): hankeen luokat
    """

    def __init__(self, root, service, margins, project_view):
        """Luo hankkeenluontinäkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            margins (dict): viitekentät hajautustaulussa:
                header (HeaderFrame): näkymän yläviitekenttä 
                footer (MarginFrame): näkymän alaviitekenttä
                left_margin (MarginFrame): näkymän vasen viitekenttä
                right_margin (MarginFrame): näkymän oikea viitekenttä
            project_view: hankenäkymä 
        """
        self._project_view = project_view
        self._project_name = None
        self._project_class = None
        self._project_description = None
        super().__init__(root=root, service=service, margins=margins)
        self._classes = self._service.get_project_service().get_project_classes("Hanke")

    def _get_class_object(self):
        for type_class in self._classes:
            if type_class.value == self._project_class.get():
                return type_class
        return None

    def _create_project_handler(self):
        self._hide_error()
        try:
            user = self._service.get_user_service().get_current_user()
            project = self._service.get_project_service().create_project(
                self._project_name.get(),
                self._get_class_object(),
                self._project_description.get("1.0", END),
                user
            )
            self._project_view(project)
        except (self._service.get_project_service().get_exceptions().ProjectHasNoTitle,
                self._service.get_project_service().get_exceptions().ProjectHasNoType,
                self._service.get_project_service().get_exceptions().ProjectHasNoOwner) as e:
            self._show_error(e.message)

    def _initialize_project_fields(self):
        name_label = ttk.Label(
            master=self._frame,
            text="Nimi*:"
        )
        name_label.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )

        self._project_name = ttk.Entry(master=self._frame)
        self._project_name.grid(
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
        self._project_class.set("Valitse luokka.")
        self._project_class.grid(
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
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.W)
        )

        self._project_description = stext.ScrolledText(master=self._frame)
        self._project_description.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        create_button = ttk.Button(
            master=self._frame,
            text="Luo",
            command=self._create_project_handler
        )
        create_button.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

        name_label = ttk.Label(
            master=self._frame,
            text="*Pakolliset tiedot"
        )
        name_label.grid(
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.W)
        )

    def _configure_window_grid(self):
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_rowconfigure(2, weight=1)
        self._root.grid_rowconfigure(3, weight=1)
        self._root.grid_rowconfigure(4, weight=1)
        self._root.grid_rowconfigure(5, weight=1)
        self._root.grid_rowconfigure(6, weight=1)
        self._root.grid_rowconfigure(7, weight=1)
        self._root.grid_rowconfigure(8, weight=1)
        self._root.grid_rowconfigure(9, weight=1)
        self._root.grid_rowconfigure(10, weight=1)

        self._root.grid_columnconfigure(0, weight=1)
        self._root.grid_columnconfigure(1, weight=1)
        self._root.grid_columnconfigure(2, weight=1)
        self._root.grid_columnconfigure(3, weight=1)
        self._root.grid_columnconfigure(4, weight=1)

    def _initialize_frame(self):
        self._configure_window_grid()

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
            self._initialize_error()
            self._initialize_project_fields()
        except self._service.get_user_service().get_exceptions().SessionNotFound as e:
            self._initialize_error()
            self._show_error(e.message)

        self._hide_error()
