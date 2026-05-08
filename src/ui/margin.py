from tkinter import ttk, constants


class MarginFrame:
    """Luokka kuvaa viitekenttäkehystä.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätään
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _row (int): rivi, jolle kehys sijoitetaan ikkunassa
            _column (int): sarake, johon kehys sijoitetaan ikkunassa
            _rowspan (int): kehyksen korkeus ikkunassa 
            _columnspan (int): kehyksen leveys ikkunassa
            _configs: käyttöliittymän ominaisuuksien arvot tiedostossa
    """

    def __init__(self, *, root, configs):
        """Luo viitekenttäkehys.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            configs: käyttöliittymän ominaisuuksien arvot tiedostossa
        """
        self._root = root
        self._frame = None
        self._row = 0
        self._column = 0
        self._rowspan = 1
        self._columnspan = 1
        self._configs = configs

    def pack(self):
        """Näyttää näkymän."""
        self._frame.grid(
            row=self._row,
            column=self._column,
            columnspan=self._columnspan,
            sticky=(constants.NS, constants.EW)
        )

    def destroy(self):
        """Poistaa näkymän."""
        self._frame.destroy()

    def configure(self, values):
        """Muokkaa viitekehyksen asetuksia.

            Args:
                values (dict): asetusten arvot hajautustaulussa:
                    row (int): rivi, jolle kehys sijoitetaan ikkunassa
                    column (int): sarake, johon kehys sijoitetaan ikkunassa
                    rowspan (int): kehyksen korkeus ikkunassa 
                    columnspan (int): kehyksen leveys ikkunassa
        """
        if "row" in values:
            self._row = values["row"]
        if "column" in values:
            self._column = values["column"]
        if "rowspan" in values:
            self._rowspan = values["rowspan"]
        if "columnspan" in values:
            self._columnspan = values["columnspan"]

        self._initialize()

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        for i in range(self._rowspan):
            self._frame.grid_rowconfigure(i, weight=1)

        for i in range(self._columnspan):
            self._frame.grid_columnconfigure(i, weight=1)

    def _initialize(self):
        self._initialize_frame()
