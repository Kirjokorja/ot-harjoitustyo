from tkinter import ttk, constants

class StartView:
    """Luokka vastaa sovelluksen aloitusnäkymästä."""
    
    def __init__(self, root):
        """Luokan konstruktori, joka luo aloitusnäkymän.

            Args:
                root: Tkinter-osanen, johon näkymä lisätään
        """
        self._root = root
        self._frame = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(side=constants.top, fill=constants.X)
    
    def destroy(self):
        """Poistaa näkymän."""
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        greeting = ttk.Label(master=self._frame, text="Tervetuloa!")

        greeting.grid(row=0, column=0)
