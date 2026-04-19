from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.front_view import FrontView
from ui.new_project_view import NewProjectView
from ui.project_view import ProjectView
from tkinter import ttk, font, constants
from services.complete_services import default_services
from ui_config import APP_NAME


class UI:
    """Luokka huolehtii sovelluksen käyttöliittymästä.

    Attribuutit:
            _root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            _current_view: käyttöliittymän näyttämä näkymä
            _services: palvelu, joka vastaa sovellusksen toiminnasta
            _style (Style): muotoilusta vastaava Tkinter-osanen
            _font (Font): sovelluksen fontista vastaava Tkinter-osanen
    """

    def __init__(self, root, services=default_services):
        """Alusta uusi käyttöliittymä.

        Muuttujat:
            root (Tk): Tkinter-osanen, johon käyttöliittymä alustetaan
            service: palvelu, joka vastaa sovellusksen toiminnasta
        """
        self._root = root
        self._current_view = None
        self._services = services
        self._style = ttk.Style()
        self._font = font.nametofont("TkDefaultFont")

    def start(self):
        """Käyttöliittymän käynnistävä metodi"""
        window_width = int(self._root.winfo_screenwidth() * 0.5)
        window_height = int(self._root.winfo_screenheight() * 0.5)
        window_width_min = int(self._root.winfo_screenwidth() * 0.15)
        window_height_min = int(self._root.winfo_screenheight() * 0.2)

        self._root.geometry(f"{window_width}x{window_height}")

        self._root.minsize(window_width_min, window_height_min)

        self._root.title(APP_NAME)

        # self._style.configure("TFrame", foreground="black", background="blue")
        self._font.configure(size=12)

        self._root.bind_all('<Control-Up>', self._upsize_event)
        self._root.bind_all('<Control-Down>', self._downsize_event)

        self._show_login_view()

    def _upsize_event(self, event):
        if self._font["size"] < 36 and self._current_view != None:
            self._font.configure(size=self._font["size"]+2)
            self._current_view.pack()

    def _downsize_event(self, event):
        if self._font["size"] > 8 and self._current_view != None:
            self._font.configure(size=self._font["size"]-2)
            self._current_view.pack()

    def _logout_handler(self):
        self._services.get_user_service().logout()
        self._back_to_login()

    def initialize_header(self, frame, user):
        if user:
            user_label = ttk.Label(
                master=frame,
                text=f"Olet kirjautunut sisään nimellä {user.username}."
            )
            user_label.grid(
                padx=5,
                pady=5,
                sticky=constants.W
            )

            front_view_button = ttk.Button(
                master=frame,
                text="Etusivu",
                command=self._show_front_view
            )
            front_view_button.grid(
                padx=10,
                pady=10,
                sticky=constants.EW
            )

            logout_button = ttk.Button(
                master=frame,
                text="Kirjaudu ulos",
                command=self._logout_handler
            )
            logout_button.grid(
                padx=5,
                pady=10,
                sticky=constants.EW
            )

            new_project_button = ttk.Button(
                master=frame,
                text="Luo maailma",
                command=self._show_new_project_view
            )
            new_project_button.grid(
                padx=5,
                pady=10,
                sticky=constants.EW
            )
        else:
            login_view_button = ttk.Button(
                master=frame,
                text="Kirjaudu sisään",
                command=self._show_login_view
            )
            login_view_button.grid(
                padx=10,
                pady=10,
                sticky=constants.EW
            )

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self):
        self._hide_current_view()
        self._current_view = LoginView(
            self._root,
            self._services.get_user_service(),
            self._show_create_user_view,
            self._show_front_view
        )
        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()
        self._current_view = CreateUserView(
            self._root,
            self._services.get_user_service(),
            self._show_login_view
        )
        self._current_view.pack()

    def _show_front_view(self):
        self._hide_current_view()
        self._current_view = FrontView(
            self._root,
            self._services,
            self._show_login_view,
            self._show_new_project_view
        )
        self._current_view.pack()

    def _show_new_project_view(self):
        self._hide_current_view()
        self._current_view = NewProjectView(
            self._root,
            self._services,
            self._show_front_view,
            self._show_login_view,
            self._show_project_view
        )
        self._current_view.pack()

    def _show_project_view(self, project):
        self._hide_current_view()
        self._current_view = ProjectView(
            self._root,
            self._services,
            project,
            self._show_front_view,
            self._show_login_view
        )
        self._current_view.pack()
