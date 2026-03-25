from tkinter import ttk, constants

class StartView:
    """Luokka vastaa sovelluksen aloitusnäkymästä."""
    
    def __init__(self, root):
        self._root = root
        self._frame = None
        
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)
    
    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        greeting = ttk.Label(master=self._frame, text="Tervetuloa!")

        greeting.grid(row=0, column=0)
