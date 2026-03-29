from tkinter import ttk, constants

class StartView:
    """Luokka vastaa sovelluksen aloitusnäkymästä.
        
        Attribuutit:
            _root (Tk): Tkinter-osanen, johon näkymä lisätää
            _frame (Frame): kehys näkymän rakenteiden ryhmittelyyn
            _create_user_view: käyttäjänluontinäkymä
    """
    
    def __init__(self, root, create_user_view):
        """Luo aloitusnäkymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon näkymä lisätään
            create_user_view: käyttäjänluontinäkymä
        """
        self._root = root
        self._frame = None
        self._create_user_view = create_user_view

        self._initialize()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.X)
    
    def destroy(self):
        """Poistaa näkymän."""
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        greeting = ttk.Label(master=self._frame, text="Tervetuloa!")

        create_user_button = ttk.Button(master=self._frame,
                                text="Rekisteröidy",
                                command=self._create_user_view
                            )
        
        greeting.grid(padx=5, pady=5)
        create_user_button.grid(padx=5, pady=5, sticky=constants.EW)
