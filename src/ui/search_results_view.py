from tkinter import ttk, constants
from utils.util_funcs import ceildiv
from ui.view import ViewBase


class SearchResultsView(ViewBase):
    """Luokka vastaa sovelluksen hakutulosten listauksesta.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätään
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: toiminnoista vastaava olio
            _message_variable (StringVar): merkkijonomuuttuja,
                joka säilyttää näytöllä näytettävää viestiä
            _message_label (Label): viestin näyttämisestä vastaava Label-olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
            _grid_size (tuple): monikko, 
                joka sisältää näkymän kehyksen ristikon rivien ja sarakkeiden määrän
            _center_column (int): ristikon keskimmäinen ruutu
            _header (HeaderFrame): näkymän yläviitekenttä 
            _message (String): näkymässä näytettävä viesti
            _message_win (Toplevel): käyttöliittymän päälle luotava ikkuna viestejä varten
            _question_answer (bool): käyttäjän vastaus kysymysikkunan kysymykseeen
            _page_size (int): sivulla kerralla näytettävien hakutulosten määrä
            _query (String): hakusana
            _result_count (int): hakutulosten kokonaismäärä
            _page (int): nykyinen hakutulossivu
            _page_count (int): tulossivujen lukumäärä
            _results (List): haun yhden sivun tulokset
            _tree (Treeview): Tkinter-osanen, joka listaa tulokset
            _tree_nav_frame (Frame): Tkinter-osanen, 
                joka sisältää tuloslistan siirtymänapit ja sivunumeron
            _project_view: hankenäkymä
            _config: käyttöliittymän ominaisuuksien arvot tiedostossa
    """

    def __init__(self, *, root, service, config, header, inputs, project_view):
        """Luo hakutulosnäkymä.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: toiminnoista vastaava olio
            config: käyttöliittymän ominaisuuksien arvot tiedostossa
            header (HeaderFrame): näkymän yläviitekenttä
            inputs (dict): dataa, jota näkymä tarvitsee
                keys:
                    message (String): näkymässä näytettävä viesti
                    query (String): hakusana
                    page (int): nykyinen hakutulossivu
            project_view: hankenäkymä  
        """
        self._page_size = 10
        self._query = inputs["query"]
        self._result_count = 0
        self._page = inputs["page"]
        self._page_count = 0
        self._results = None
        self._tree = None
        self._tree_nav_frame = None
        self._project_view = project_view
        super().__init__(
            root=root, service=service,
            header=header,
            message=inputs["message"],
            config=config
        )

    def _previous_page_handler(self):
        self._tree.destroy()
        self._tree = None
        self._tree_nav_frame.destroy()
        self._tree_nav_frame = None
        self._page -= 1
        self.initialize()
        self.pack()

    def _next_page_handler(self):
        self._tree.destroy()
        self._tree = None
        self._tree_nav_frame.destroy()
        self._tree_nav_frame = None
        self._page += 1
        self.initialize()
        self.pack()

    def _double_click_item(self, event):
        item = self._tree.selection()
        if item:
            project = self._service.get_project_service(
            ).get_project(project_id=item[0])
            self._project_view(
                message=None,
                project=project,
                query=self._query,
                page=self._page
            )

    def _initialize_results(self):
        self._result_count = self._service.get_project_service(
        ).count_projects(query=self._query)
        self._page_count = ceildiv(self._result_count, self._page_size)
        self._page_count = max(self._page_count, 1)
        self._page = max(self._page, 1)
        self._page = min(self._page, self._page_count)
        self._results = self._service.get_project_service().search_projects(
            query=self._query, page=self._page, page_size=self._page_size)

    def _initialize_tree(self):
        self._tree = ttk.Treeview(master=self._frame)
        columns = []
        for i in range(self._config.RESULT_LIST_NUMBER_OF_COLUMNS):
            columns.append(f"col_{i}")
        self._tree.configure(columns=columns)
        self._tree.column("#0", width=0, stretch=constants.NO)

        column_names = self._config.RESULT_LIST_COLUMN_NAMES
        for i in range(self._config.RESULT_LIST_NUMBER_OF_COLUMNS):
            self._tree.heading(f"col_{i}", text=column_names[i])

        for item in self._results:
            self._tree.insert(parent="", index=constants.END, iid=item.p_id, values=(
                item.title, item.p_type.value, item.owner.username))

        self._tree.bind(
            sequence=self._config.RESULT_LIST_OPEN_ITEM_TRIGGER,
            func=self._double_click_item
        )

        self._tree.grid(
            row=2,
            columnspan=self._grid_size[0],
            sticky=constants.NSEW
        )

        self._tree_nav_frame = ttk.Frame(master=self._frame)
        self._initialize_tree_nav()
        self._tree_nav_frame.grid(
            column=self._grid_size[0]//2,
            sticky=constants.NSEW
        )

    def _initialize_tree_nav(self):
        if self._page > 1:
            self._tree_nav_frame.columnconfigure(2, weight=1)
            previous_button = ttk.Button(
                master=self._tree_nav_frame,
                text="<-",
                command=self._previous_page_handler
            )
            previous_button.grid(
                padx=5,
                pady=5,
                row=0,
                column=0,
                columnspan=1,
                sticky=(constants.NS, constants.W)
            )

        pages_label = ttk.Label(
            master=self._tree_nav_frame,
            text=f"({self._page}/{self._page_count})",
            anchor=constants.CENTER
        )
        pages_label.grid(
            padx=5,
            pady=5,
            row=0,
            column=1,
            columnspan=1,
            sticky=constants.NSEW
        )
        self._tree_nav_frame.columnconfigure(1, weight=1)

        if self._page is not self._page_count:
            self._tree_nav_frame.columnconfigure(0, weight=1)
            next_button = ttk.Button(
                master=self._tree_nav_frame,
                text="->",
                command=self._next_page_handler
            )
            next_button.grid(
                padx=5,
                pady=5,
                row=0,
                column=2,
                columnspan=1,
                sticky=(constants.NS, constants.E)
            )

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()

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
            if self._message:
                self._initialize_message()
                self._show_message(self._message)
            self._initialize_results()
            self._initialize_tree()
            self._hide_message()
        except self._service.get_user_service().get_exceptions().SessionNotFound as e:
            self._initialize_error()
            self._show_error(e.message)

        self._hide_error()
