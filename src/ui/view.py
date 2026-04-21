from tkinter import ttk, constants, StringVar


class ViewBase:
    """Luokka kuvaa käyttöliittymänäkymää.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätään
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: käyttäjätoiminnoista vastaava olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
            _grid_size (tuple): monikko, joka sisältää näkymän kehyksen ristikon rivien ja sarakkeiden määrän
            _margins (dict): viitekentät hajautustaulussa:
                header (HeaderFrame): näkymän yläviitekenttä 
                footer (MarginFrame): näkymän alaviitekenttä
                left_margin (MarginFrame): näkymän vasen viitekenttä
                right_margin (MarginFrame): näkymän oikea viitekenttä
    """

    def __init__(self, root, service, margins):
        """Luo näkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: käyttäjätoiminnoista vastaava olio
            margins (dict): viitekentät hajautustaulussa:
                header (HeaderFrame): näkymän yläviitekenttä 
                footer (MarginFrame): näkymän alaviitekenttä
                left_margin (MarginFrame): näkymän vasen viitekenttä
                right_margin (MarginFrame): näkymän oikea viitekenttä
        """
        self._root = root
        self._service = service
        self._frame =None
        self._error_variable = None
        self._error_label = None
        self._grid_size = None
        self._margins = margins

    def pack(self):
        """Näyttää näkymän."""
        self._margins["header"].pack()
        self._frame.grid(
            row=2,
            column=2,
            rowspan=2,
            columnspan=1,
            ipadx=90,
            sticky=(constants.NS, constants.EW)
        )

    def destroy(self):
        """Poistaa näkymän."""
        self._margins["header"].destroy()
        self._frame.destroy()

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_error(self):
        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red",
            anchor="center"
        )
        self._error_label.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
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
        self._frame.grid_rowconfigure(7, weight=1)

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)

        self._grid_size = self._frame.grid_size()

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()
        self._margins["header"].configure(
            {"row":0,
            "column":0,
            "rowspan":2,
            "columnspan":self._root.grid_size()[0]}
        )
        self._initialize_error()
        self._hide_error()
