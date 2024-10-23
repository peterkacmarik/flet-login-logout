import flet as ft
import requests
import requests.cookies

# from frontend.core.config import frontend_settings


class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/")
        
        self.page = page
        # self.check_protected_access()
        
        # Nastavenie zásuvky hneď pri inicializácii
        self.drawer = self.build_drawer()
        self.appbar = self.build_appbar()
        self.navigation_bar = self.build_navigation_bar()
        
        # Hlavný obsah stránky
        self.controls = [
            self.appbar,
            ft.Container(
                border=ft.border.all(3, ft.colors.RED),
                # content=ft.Row(
                #     controls=[
                #         ft.Icon(ft.icons.HOME_OUTLINED),
                #         ft.Text("Home"),
                #         ft.Text("Container", size=20, text_align=ft.TextAlign.CENTER),    
                #     ],
                #     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                #     vertical_alignment=ft.CrossAxisAlignment.CENTER,
                # ),
            ),
            ft.Text("Welcome to the protected area!", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            self.navigation_bar,
        ]

    
    def check_protected_access(self):
        try:
            # Získanie JWT tokenu z cookies prehliadača (ak existuje)
            session = requests.Session()
            
            # Získanie cookies z prehliadača a ich pridanie do session
            browser_cookies = self.page.client_storage.get("jwt_token")
            if browser_cookies:
                session.cookies.set("jwt_token", browser_cookies)
            
            response = session.get("http://127.0.0.1:8000/api/v1/auth/verify-token")
            
            if response.status_code == 200:
                print("User is authenticated:", response.json())
            else:
                print("Access denied. Redirecting to login.")
                print(response.json())
                self.page.go("/login")
        except Exception as e:
            print(f"Error checking protected access: {e}")
            self.page.go("/login")
            
    
    def build_appbar(self) -> ft.AppBar:
        self.page.appbar = ft.AppBar(
            leading=ft.IconButton(icon=ft.icons.MENU, on_click=self.open_drawer),  # Zmena metódy
            title=ft.Text("Flet App"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            center_title=False,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=lambda _: self.change_theme()),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Profile"),
                        ft.PopupMenuItem(text="Help"),
                        ft.PopupMenuItem(text="Settings"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(text="Logout", on_click=self.handle_logout),
                    ]
                )
            ],
        )
        return self.page.appbar
    
    
    def handle_logout(self, e):
        try:
            # Získanie a poslanie cookies zo session
            session = requests.Session()
            browser_cookies = self.page.client_storage.get("jwt_token")
            if browser_cookies:
                session.cookies.set("jwt_token", browser_cookies)
                
            response = session.get("http://127.0.0.1:8000/api/v1/auth/logout")

            if response.status_code == 200:
                # Vymazanie cookies z client storage
                self.page.client_storage.remove("jwt_token")
                self.page.go("/login")
            else:
                print("Logout failed:", response.json())
        except Exception as e:
            print(f"Logout error: {e}")
    

    def open_drawer(self, e: ft.ControlEvent) -> None:
        self.drawer.open = True
        self.drawer.update()
    
    
    def build_drawer(self) -> ft.NavigationDrawer:
        return ft.NavigationDrawer(
            selected_index=0,
            on_change=self.handle_change,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Item 1",
                    icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                    label="Item 2",
                    selected_icon=ft.icons.MAIL,
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                    label="Item 3",
                    selected_icon=ft.icons.PHONE,
                ),
            ],)
        

    def build_navigation_bar(self) -> ft.NavigationBar:
        self.page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    label="Home",
                    selected_icon=ft.icons.HOME,
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.PERSON_OUTLINED,
                    label="Profile",
                    selected_icon=ft.icons.PERSON,
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    label="Settings",
                    selected_icon=ft.icons.SETTINGS,
                ),
            ],
        )
        return self.page.navigation_bar




    def check_item_clicked(self, e):
        e.control.checked = not e.control.checked
        self.page.update()
        
    def change_theme(self, e=None):
        try:
            if self.page.theme_mode == ft.ThemeMode.DARK:
                self.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                self.page.theme_mode = ft.ThemeMode.DARK
            self.page.update()
        except Exception as e:
            print(f"Error changing theme: {e}")

    def handle_change(self, e):
        try:
            print(f"Tab selected: {e.control.selected_index}")
            self.page.update()
        except Exception as e:
            print(f"Error handling tab change: {e}")
            
        