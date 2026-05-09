from tkinter import font
from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.front_view import FrontView
from ui.create_project_view import CreateProjectView
from ui.edit_project_view import EditProjectView
from ui.project_view import ProjectView
from ui.search_results_view import SearchResultsView
from ui.header import HeaderFrame
from services.complete_services import default_services
import config_ui as default_config


class UI:
    """Luokka huolehtii sovelluksen käyttöliittymästä.

    Attributes:
            _root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            _current_view: käyttöliittymän näyttämä näkymä
            _service: palvelu, joka vastaa sovellusksen toiminnasta
            _font (Font): sovelluksen fontista vastaava Tkinter-osanen
            _config: käyttöliittymän ominaisuuksien arvot tiedostossa
    """

    def __init__(self, root, service=default_services, config=default_config):
        """Alusta uusi käyttöliittymä.

        Args:
            root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            service: palvelu, joka vastaa sovellusksen toiminnasta
            config: käyttöliittymän ominaisuuksien arvot tiedostossa
        """
        self._root = root
        self._current_view = None
        self._service = service
        self._font = None
        self._config = config

    def start(self):
        """Käyttöliittymän käynnistävä metodi"""
        window_width = int(self._root.winfo_screenwidth()
                           * self._config.WINDOW_WIDTH_SCALE)
        window_height = int(self._root.winfo_screenheight()
                            * self._config.WINDOW_HEIGHT_SCALE)
        window_width_min = int(self._root.winfo_screenwidth()
                               * self._config.WINDOW_MIN_WIDTH_SCALE)
        window_height_min = int(
            self._root.winfo_screenheight() * self._config.WINDOW_MIN_HEIGHT_SCALE)

        self._root.geometry(f"{window_width}x{window_height}")
        self._root.minsize(window_width_min, window_height_min)
        self._configure_window_grid()

        self._root.title(self._config.APP_NAME)

        self._font = font.nametofont(self._config.DEFAULT_FONT)
        self._font.configure(size=self._config.DEFAULT_FONT_SIZE)

        self._root.bind_all(
            sequence=self._config.SCALE_FONT_BIGGER_TRIGGER,
            func=self._upsize_event
        )
        self._root.bind_all(
            sequence=self._config.SCALE_FONT_SMALLER_TRIGGER,
            func=self._downsize_event
        )

        self._show_login_view()

    def _configure_window_grid(self):
        for i in range(8):
            self._root.grid_rowconfigure(i, weight=1)

        for i in range(5):
            self._root.grid_columnconfigure(i, weight=1)

    def _upsize_event(self, event):
        if (self._font["size"] < self._config.SCALE_FONT_MAX_SIZE
                and self._current_view is not None):
            self._font.configure(
                size=self._font["size"]+self._config.SCALE_FONT_INCREMENT_SIZE
            )
            self._current_view.pack()

    def _downsize_event(self, event):
        if (self._font["size"] > self._config.SCALE_FONT_MIN_SIZE
                and self._current_view is not None):
            self._font.configure(
                size=self._font["size"]-self._config.SCALE_FONT_INCREMENT_SIZE
            )
            self._current_view.pack()

    def _logout_handler(self):
        self._service.get_user_service().logout()
        self._show_login_view(self._config.LOGOUT_MSG)

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _create_header(self):
        header_buttons = {
            "nav_button_1_logged_in": self._show_front_view,
            "nav_button_1_logged_out": self._show_login_view,
            "nav_button_2": self._show_create_project_view,
            "nav_button_3": self._logout_handler
        }
        header = HeaderFrame(
            root=self._root,
            service=self._service,
            config=self._config,
            buttons=header_buttons,
            search_results_view=self._show_search_results_view
        )
        return header

    def _show_login_view(self, message=None):
        self._hide_current_view()
        header = self._create_header()
        views = {
            "create_user_view": self._show_create_user_view,
            "front_view": self._show_front_view
        }
        self._current_view = LoginView(
            root=self._root,
            service=self._service,
            config=self._config,
            header=header,
            views=views,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_create_user_view(self, message=None):
        self._hide_current_view()
        header = self._create_header()
        self._current_view = CreateUserView(
            root=self._root,
            service=self._service,
            config=self._config,
            header=header,
            back_to_start_view=self._show_login_view,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_front_view(self, message=None):
        self._hide_current_view()
        header = self._create_header()
        self._current_view = FrontView(
            root=self._root,
            service=self._service,
            header=header,
            message=message,
            config=self._config
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_create_project_view(self, message=None):
        self._hide_current_view()
        header = self._create_header()
        self._current_view = CreateProjectView(
            root=self._root,
            service=self._service,
            config=self._config,
            header=header,
            project_view=self._show_project_view,
            message=message
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_project_view(self, message, project, query, page):
        self._hide_current_view()
        header = self._create_header()
        views = {
            "edit_project_view": self._show_edit_project_view,
            "back_to_front_view": self._show_front_view,
            "back_to_search_results": self._show_search_results_view
        }
        inputs = {
            "message": message,
            "project": project,
            "query": query,
            "page": page
        }
        self._current_view = ProjectView(
            root=self._root,
            service=self._service,
            config=self._config,
            header=header,
            views=views,
            inputs=inputs
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_edit_project_view(self, message, project, query, page):
        self._hide_current_view()
        header = self._create_header()
        inputs = {
            "project": project,
            "message": message,
            "query": query,
            "page": page
        }
        self._current_view = EditProjectView(
            root=self._root,
            service=self._service,
            config=self._config,
            header=header,
            project_view=self._show_project_view,
            inputs=inputs
        )
        self._current_view.initialize()
        self._current_view.pack()

    def _show_search_results_view(self, message, query, page):
        self._hide_current_view()
        header = self._create_header()
        inputs = {
            "message": message,
            "query": query,
            "page": page
        }
        self._current_view = SearchResultsView(
            root=self._root,
            service=self._service,
            config=self._config,
            header=header,
            inputs=inputs,
            project_view=self._show_project_view
        )
        self._current_view.initialize()
        self._current_view.pack()
