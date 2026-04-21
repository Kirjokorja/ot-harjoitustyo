from tkinter import ttk, constants, scrolledtext as stext, END
from ui.session_view import SessionView


class ProjectView(SessionView):
    """Luokka vastaa hankenäkymästä.

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
            _user (User): istunnon haltijan käyttäjäolio
            _project (Project): näytettävä hanke
    """

    def __init__(self, root, service, project, margins):
        """Näytä hanke.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            project (Project): näytettävä hanke
            margins (dict): viitekentät hajautustaulussa:
                header (HeaderFrame): näkymän yläviitekenttä 
                footer (MarginFrame): näkymän alaviitekenttä
                left_margin (MarginFrame): näkymän vasen viitekenttä
                right_margin (MarginFrame): näkymän oikea viitekenttä
        """
        super().__init__(root=root, service=service, margins=margins)
        self._project = project

    def _initialize_project_fields(self):
        name_label = ttk.Label(
            master=self._frame,
            text=self._project.title
        )
        name_label.grid(
            row=1,
            padx=5,
            pady=5,
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
            sticky=(constants.NS, constants.W)
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
            sticky=(constants.NS, constants.W)
        )

        description = stext.ScrolledText(master=self._frame)
        description.insert(END, self._project.description)
        description.grid(
            column=self._grid_size[0]//2,
            row=3,
            padx=5,
            pady=5,
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
            sticky=(constants.NS, constants.W)
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
            sticky=(constants.NS, constants.EW)
        )

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)

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
