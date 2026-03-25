from ui.start_view import StartView

class UI:
    """Luokka huolehtii sovelluksen käyttöliittymästä."""

    def __init__(self, root):
        self._root = root
        self._current_view = None
    
    def start(self):
        """Käyttöliittymän käynnistävä metodi"""
        self._show_start_view()
    
    def _destroy_current_view(self):
        if self._current_view:
            self._current_view.destroy()
    
    def _show_start_view(self):
        self._current_view = StartView(
            self._root
        )
        self._current_view.pack()
        