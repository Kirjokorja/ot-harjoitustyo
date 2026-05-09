from tkinter import ttk, constants, StringVar, Toplevel
from math import floor


class ViewBase:
    """Luokka kuvaa käyttöliittymänäkymää.

        Attributes:
            _root (Tk): Tkinter-osanen, johon näkymä lisätään
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _service: käyttäjätoiminnoista vastaava olio
            _message_variable (StringVar): merkkijonomuuttuja, joka säilyttää näytöllä näytettävää viestiä
            _message_label (Label): viestin näyttämisestä vastaava Label-olio
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
            _grid_size (tuple): monikko, joka sisältää näkymän kehyksen ristikon rivien ja sarakkeiden määrän
            _header (HeaderFrame): näkymän yläviitekenttä
            _message (String): näkymässä näytettävä viesti
            _message_win (Toplevel): käyttöliittymän päälle luotava ikkuna viestejä varten
            _question_answer (bool): käyttäjän vastaus kysymysikkunan kysymykseeen
            _configs: käyttöliittymän ominaisuuksien arvot tiedostossa
    """

    def __init__(self, *, root, service, header, message, configs):
        """Luo näkymä.

        Args:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            service: käyttäjätoiminnoista vastaava olio
            header (HeaderFrame): näkymän yläviitekenttä
            message (String): näkymässä näytettävä viesti
            configs: käyttöliittymän ominaisuuksien arvot tiedostossa
        """
        self._root = root
        self._service = service
        self._frame = None
        self._message_variable = None
        self._message_label = None
        self._error_variable = None
        self._error_label = None
        self._grid_size = None
        self._header = header
        self._message = message
        self._qusetion_win = None
        self._question_answer = None
        self._configs = configs

    def pack(self):
        """Näyttää näkymän."""
        self._header.pack()
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
        self._header.destroy()
        self._frame.destroy()

    def _show_message(self, message):
        self._message_variable.set(message)
        self._message_label.grid()

    def _hide_message(self):
        self._message_label.grid_remove()

    def _initialize_message(self):
        self._message_variable = StringVar(self._frame)
        self._message_label = ttk.Label(
            master=self._frame,
            textvariable=self._message_variable,
            anchor=constants.CENTER
        )
        self._message_label.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

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
            anchor=constants.CENTER
        )
        self._error_label.grid(
            padx=5,
            pady=5,
            columnspan=self._grid_size[0],
            sticky=(constants.NS, constants.EW)
        )

    def _yes_handler(self):
        self._question_answer = True
        self._qusetion_win.destroy()
        self._qusetion_win = None
        self._question_answer_handler()

    def _no_handler(self):
        self._question_answer = False
        self._qusetion_win.destroy()
        self._qusetion_win = None
        self._question_answer_handler()

    def _question_answer_handler(self):
        pass

    def _question_window(self, title, message, yes_text, no_text):
        self._qusetion_win = Toplevel(master=self._root)

        win_width = int(
            self._root.winfo_screenwidth() * self._configs.Q_WIN_MIN_WIDTH_SCALE
        )
        win_height = int(
            self._root.winfo_screenheight() * self._configs.Q_WIN_MIN_HEIGHT_SCALE
        )
        win_offset_x = (self._root.winfo_x() +
                        floor(self._root.winfo_width()*self._configs.Q_WIN_X_REL_POS_TO_MASTER) -
                        win_width//2)
        win_offset_y = (self._root.winfo_y() +
                        floor(self._root.winfo_height()*self._configs.Q_WIN_Y_REL_POS_TO_MASTER) -
                        win_height//2)

        self._qusetion_win.geometry(f"{win_width}x{win_height}")
        self._qusetion_win.geometry(f"+{win_offset_x}+{win_offset_y}")
        self._qusetion_win.minsize(win_width, win_height)
        self._qusetion_win.title(title)

        self._qusetion_win.grid_columnconfigure(0, weight=1)
        self._qusetion_win.grid_columnconfigure(1, weight=1)

        message_label = ttk.Label(
            master=self._qusetion_win,
            text=message,
            anchor=constants.CENTER
        )
        message_label.grid(
            padx=10,
            pady=10,
            columnspan=self._qusetion_win.grid_size()[0],
            sticky=(constants.NS, constants.EW)
        )
        yes_button = ttk.Button(
            master=self._qusetion_win,
            text=yes_text,
            command=self._yes_handler
        )
        yes_button.grid(
            column=0,
            row=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )
        no_button = ttk.Button(
            master=self._qusetion_win,
            text=no_text,
            command=self._no_handler
        )
        no_button.grid(
            column=1,
            row=1,
            padx=5,
            pady=5,
            sticky=(constants.NS, constants.EW)
        )

    def _initialize_frame(self):
        self._frame = ttk.Frame(master=self._root)

        for i in range(8):
            self._frame.grid_rowconfigure(i, weight=1)

        for i in range(3):
            self._frame.grid_columnconfigure(i, weight=1)

        self._grid_size = self._frame.grid_size()

    def initialize(self):
        """Alusta näkymä."""
        self._initialize_frame()
        self._header.configure(
            {"row": 0,
             "column": 0,
             "rowspan": 1,
             "columnspan": self._root.grid_size()[0]}
        )
        self._initialize_error()

        self._initialize_message()
        self._show_message(self._message)

        self._hide_error()
