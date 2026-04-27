from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.front_view import FrontView
from ui.create_project_view import CreateProjectView
from ui.edit_project_view import EditProjectView
from ui.project_view import ProjectView
from ui.margin import MarginFrame
from ui.header import HeaderFrame
from tkinter import ttk, font
from services.complete_services import default_services
from ui_config import APP_NAME


class UI:
    """Luokka huolehtii sovelluksen käyttöliittymästä.

    Attributes:
            _root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            _current_view: käyttöliittymän näyttämä näkymä
            _service: palvelu, joka vastaa sovellusksen toiminnasta
            _font (Font): sovelluksen fontista vastaava Tkinter-osanen
    """

    def __init__(self, root, service=default_services):
        """Alusta uusi käyttöliittymä.

        Args:
            root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            service: palvelu, joka vastaa sovellusksen toiminnasta
        """
        self._root = root
        self._current_view = None
        self._service = service
        self._font = font.nametofont("TkDefaultFont")

    def start(self):
        """Käyttöliittymän käynnistävä metodi"""
        window_width = int(self._root.winfo_screenwidth() * 0.6)
        window_height = int(self._root.winfo_screenheight() * 0.6)
        window_width_min = int(self._root.winfo_screenwidth() * 0.12)
        window_height_min = int(self._root.winfo_screenheight() * 0.22)

        self._root.geometry(f"{window_width}x{window_height}")
        self._root.minsize(window_width_min, window_height_min)
        self._configure_window_grid()

        self._root.title(APP_NAME)

        self._font.configure(size=12)

        self._root.bind_all('<Control-Up>', self._upsize_event)
        self._root.bind_all('<Control-Down>', self._downsize_event)

        self._show_login_view()

    def _configure_window_grid(self):
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_rowconfigure(2, weight=1)
        self._root.grid_rowconfigure(3, weight=1)
        self._root.grid_rowconfigure(4, weight=1)
        self._root.grid_rowconfigure(5, weight=1)
        self._root.grid_rowconfigure(6, weight=1)
        self._root.grid_rowconfigure(7, weight=1)
        self._root.grid_rowconfigure(8, weight=1)

        self._root.grid_columnconfigure(0, weight=1)
        self._root.grid_columnconfigure(1, weight=1)
        self._root.grid_columnconfigure(2, weight=1)
        self._root.grid_columnconfigure(3, weight=1)
        self._root.grid_columnconfigure(4, weight=1)

    def _upsize_event(self, event):
        if self._font["size"] < 36 and self._current_view != None:
            self._font.configure(size=self._font["size"]+2)
            self._current_view.pack()

    def _downsize_event(self, event):
        if self._font["size"] > 8 and self._current_view != None:
            self._font.configure(size=self._font["size"]-2)
            self._current_view.pack()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self, message=None):
        self._hide_current_view()
        margins = {
            "header": HeaderFrame(
                root=self._root,
                service=self._service,
                back_to_front_view=self._show_front_view,
                back_to_login_view=self._show_login_view,
                new_project_view=self._show_create_project_view
            ),
            "footer": MarginFrame(root=self._root),
            "left_margin": MarginFrame(root=self._root),
            "right_margin": MarginFrame(root=self._root)
        }
        self._current_view = LoginView(
            root=self._root,
            service=self._service,
            margins=margins,
            create_user_view=self._show_create_user_view,
            front_view=self._show_front_view,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_create_user_view(self, message=None):
        self._hide_current_view()
        margins = {
            "header": HeaderFrame(
                root=self._root,
                service=self._service,
                back_to_front_view=self._show_front_view,
                back_to_login_view=self._show_login_view,
                new_project_view=self._show_create_project_view
            ),
            "footer": MarginFrame(root=self._root),
            "left_margin": MarginFrame(root=self._root),
            "right_margin": MarginFrame(root=self._root)
        }
        self._current_view = CreateUserView(
            root=self._root,
            service=self._service,
            margins=margins,
            back_to_start_view=self._show_login_view,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_front_view(self, message=None):
        self._hide_current_view()
        margins = {
            "header": HeaderFrame(
                root=self._root,
                service=self._service,
                back_to_front_view=self._show_front_view,
                back_to_login_view=self._show_login_view,
                new_project_view=self._show_create_project_view
            ),
            "footer": MarginFrame(root=self._root),
            "left_margin": MarginFrame(root=self._root),
            "right_margin": MarginFrame(root=self._root)
        }
        self._current_view = FrontView(
            root=self._root,
            service=self._service,
            margins=margins,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_create_project_view(self, message=None):
        self._hide_current_view()
        margins = {
            "header": HeaderFrame(
                root=self._root,
                service=self._service,
                back_to_front_view=self._show_front_view,
                back_to_login_view=self._show_login_view,
                new_project_view=self._show_create_project_view
            ),
            "footer": MarginFrame(root=self._root),
            "left_margin": MarginFrame(root=self._root),
            "right_margin": MarginFrame(root=self._root)
        }
        self._current_view = CreateProjectView(
            root=self._root,
            service=self._service,
            margins=margins,
            project_view=self._show_project_view,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_project_view(self, message, project):
        self._hide_current_view()
        margins = {
            "header": HeaderFrame(
                root=self._root,
                service=self._service,
                back_to_front_view=self._show_front_view,
                back_to_login_view=self._show_login_view,
                new_project_view=self._show_create_project_view
            ),
            "footer": MarginFrame(root=self._root),
            "left_margin": MarginFrame(root=self._root),
            "right_margin": MarginFrame(root=self._root)
        }
        view_params = {
            "edit_project_view": self._show_edit_project_view,
            "back_to_front_view": self._show_front_view
        }
        self._current_view = ProjectView(
            root=self._root,
            service=self._service,
            project=project,
            margins=margins,
            view_params=view_params,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_edit_project_view(self, message, project):
        self._hide_current_view()
        margins = {
            "header": HeaderFrame(
                root=self._root,
                service=self._service,
                back_to_front_view=self._show_front_view,
                back_to_login_view=self._show_login_view,
                new_project_view=self._show_create_project_view
            ),
            "footer": MarginFrame(root=self._root),
            "left_margin": MarginFrame(root=self._root),
            "right_margin": MarginFrame(root=self._root)
        }
        self._current_view = EditProjectView(
            root=self._root,
            service=self._service,
            margins=margins,
            project_view=self._show_project_view,
            project=project,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()
