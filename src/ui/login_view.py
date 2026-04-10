from tkinter import ttk, constants, StringVar
import ui.ui_constructs as constructs


class LoginView:
    """Luokka vastaa sovelluksen kirjautumisnäkymästä.

        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _user_service: käyttäjätoiminnoista vastaava olio
            _create_user_view: käyttäjänluontinäkymä
            _front_view: seovelluksen etusivu kirjauduttua
            _password (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan 
            _password_confirm (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan tarkistusta varten
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
    """

    def __init__(self, root, user_service, create_user_view, front_view):
        """Luo kirjautumisnäkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            user_service: käyttäjätoiminnoista vastaava olio
            create_user_view: käyttäjänluontinäkymä
            front_view: seovelluksen etusivu kirjauduttua
        """
        self._root = root
        self._user_service = user_service
        self._create_user_view = create_user_view
        self._front_view = front_view
        self._frame = None
        self._username = None
        self._password = None
        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Poistaa näkymän."""
        self._frame.destroy()

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove() 

    def _login_handler(self):
        self._hide_error()
        username = self._username.get()
        password = self._password.get()

        try:
            self._user_service.login(username, password)
            self._front_view()
        except self._user_service.get_exceptions().InvalidCredentials as e:
            self._show_error(e.message)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        
        greeting = ttk.Label(master=self._frame, text="Tervetuloa!")

        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(master=self._frame,
                                      textvariable=self._error_variable,
                                      foreground="red"
                                      )

        self._error_label.grid(padx=5, pady=5)

        self._username = constructs.initialize_input_field(frame=self._frame, text="Käyttäjänimi", secure=False)
        self._password = constructs.initialize_input_field(frame=self._frame, text="Salasana", secure=True)
        
        login_button = ttk.Button(master=self._frame,
                                        text="Kirjaudu",
                                        command=self._login_handler
                                        )
         
        create_user_button = ttk.Button(master=self._frame,
                                        text="Rekisteröidy",
                                        command=self._create_user_view
                                        )

        greeting.grid(padx=5, pady=5)
        login_button.grid(padx=5, pady=5, sticky=constants.EW)
        create_user_button.grid(padx=5, pady=5, sticky=constants.EW)

        self._hide_error()
