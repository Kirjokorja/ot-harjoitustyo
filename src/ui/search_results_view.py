from tkinter import ttk, constants
from utils.util_funcs import ceildiv
from ui.view import ViewBase


class SearchResultsView(ViewBase):
    """Luokka vastaa sovelluksen hakutulosten listauksesta.

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
            _page_size (int): sivulla kerralla näytettävien hakutulosten määrä
            _query (String): hakusana
            _result_count (int): hakutulosten kokonaismäärä
            _page (int): nykyinen hakutulossivu
            _page_count (int): tulossivujen lukumäärä
            _results (List): haun yhden sivun tulokset
            _tree (Treeview): Tkinter-osanen, joka listaa tulokset
            _project_view: hankenäkymä
    """

    def __init__(self, root, service, margins, inputs, project_view):
        """Luo hakutulosnäkymä.

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
            query (String): hakusana
            project_view: hankenäkymä
        """
        self._page_size = 10
        self._query = inputs["query"]
        self._result_count = 0
        self._page = inputs["page"]
        self._page_count = 0
        self._results = None
        self._tree = None
        self._project_view = project_view
        super().__init__(root=root, service=service,
                         margins=margins, message=inputs["message"])

    def _previous_page_handler(self):
        self._page -= 1
        self.initialize()

    def _next_page_handler(self):
        self._page += 1
        self.initialize()

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
        self._tree.configure(columns=("title", "class", "owner"))
        self._tree.column("#0", width=0, stretch=constants.NO)

        self._tree.heading("title", text="Nimi")
        self._tree.heading("class", text="Luokka")
        self._tree.heading("owner", text="Haltija")

        for item in self._results:
            self._tree.insert(parent="", index=constants.END, iid=item.p_id, values=(
                item.title, item.p_type.value, item.owner.username))

        self._tree.bind(sequence="<Double-1>", func=self._double_click_item)

        self._tree.grid(
            columnspan=self._grid_size[0],
            sticky=constants.NSEW
        )

        if self._page > 1:
            previous_button = ttk.Button(
                master=self._frame,
                text="<-",
                command=self._previous_page_handler
            )
            previous_button.grid(
                sticky=(constants.NS, constants.E)
            )

        pages_label = ttk.Label(
            master=self._frame,
            text=f"({self._page}/{self._page_count})",
            anchor="center"
        )
        pages_label.grid(
            column=self._grid_size[0]//2,
            sticky=constants.NSEW
        )

        if self._page is not self._page_count:
            next_button = ttk.Button(
                master=self._frame,
                text="->",
                command=self._next_page_handler
            )
            next_button.grid(
                sticky=(constants.NS, constants.W)
            )

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()

        try:
            self._service.get_user_service().get_current_user()
            self._margins["header"].configure(
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
