from tkinter import ttk, constants, StringVar
from bcrypt import gensalt, hashpw

class CreateUserView:
    """Luokka vastaa sovelluksen käyttäjänluontinäkymästä.
        
        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _user_service (UserService): käyttäjään liityvistä toiminnoista vastaava olio
            _back_to_start_view: metodi, joka palauttaa alkunäkymän
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _username (Entry): Entry-olio, joka säilyttää käyttäjän antaman käyttäjätunnuksen
            _password (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan 
            _password_confirm (Entry): Entry-olio, joka säilyttää käyttäjän antaman salasanan tarkistusta varten
            _error_variable (StringVar): merkkijonomuuttuja, joka säilyttää virheilmoituksen viestiä
            _error_label (Label): virheilmoituksesen näyttämisestä vastaava Label-olio
    """
    
    def __init__(self, root, user_service, back_to_start_view, ):
        """Alusta käyttäjänluontinäkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            user_service (UserService): käyttäjään liityvistä toiminnoista vastaava olio
            back_to_start_view: metodi, joka palauttaa alkunäkymän
        """
        self._root = root
        self._user_service = user_service
        self._back_to_start_view = back_to_start_view
        self._frame = None
        self._username = None
        self._password = None
        self._password_confirm = None
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

    def _create_user_handle(self):
        username = self._username.get()
        password = self._password.get()
        password_confirm =self._password_confirm.get()

        if len(username) == 0:
            self._show_error("Käyttäjänimi on liian lyhyt.")
            return
        if len(password) < 8:
            self._show_error("Salasana on liian lyhyt.")
            return
        if password_confirm != password:
            self._show_error("Salasanat eivät täsmää.")
            return
        
        salt = gensalt()
        bytes = password.encode("utf-8")
        password_hash = hashpw(bytes, salt)

        try:
            self._user_service.create_user(username, password_hash)
            self._back_to_start_view
        except self._user_service.exceptions.UserAlreadyExists as e:
            self._show_error(e.message)
        
    def _initialize_input_field(self, text, secure):
        label = ttk.Label(master=self._frame, text=text)

        if secure == True:
            entry = ttk.Entry(master=self._frame, show="*")
        else:
            entry = ttk.Entry(master=self._frame)
        
        label.grid(padx=5, pady=5, sticky=constants.W)
        entry.grid(padx=5, pady=5, sticky=constants.EW)

        return entry 

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        
        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(master=self._frame,
                                textvariable=self._error_variable,
                                foreground="red"
                            )

        self._error_label.grid(padx=5, pady=5)

        self._username = self._initialize_input_field("Käyttäjänimi", False)
        self._password = self._initialize_input_field("Salasana (min 8 merkkiä)", True)
        self._password_confirm = self._initialize_input_field("Salasana uudestaan", True)

        create_user_button = ttk.Button(master=self._frame,
                                text="Luo",
                                command=self._create_user_handle
                            )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)
        create_user_button.grid(padx=5, pady=5, sticky=constants.EW)

        self._hide_error()
