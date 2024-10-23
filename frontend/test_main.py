# Vstupný bod pre Flet (alebo iný frontend framework)


import flet as ft

from views.login import LoginView
# from views.dashboard import DashboardView
# from views.profile import ProfileView
from views.register import RegisterView
# from views.forgot import ForgotView
from views.home import HomeView


def main(page: ft.Page):
    page.window.always_on_top = True
    page.title = "Flet App LILY"
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.window_width = 800
    # page.window_height = 600
    page.padding = ft.padding.all(0)
    # page.window_width = 400
    
    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.clear()
            page.views.append(HomeView(page))
            
        # elif page.route == "/dashboard":
        #     page.views.clear()
        #     page.add(ft.Text("Dashboard"))
            
        # elif page.route == "/profile":
        #     page.views.clear()
        #     page.add(ft.Text("Profile"))
            
        elif page.route == "/login":
            page.views.clear()
            page.views.append(LoginView(page))
            
        elif page.route == "/register":
            page.views.clear()
            page.views.append(RegisterView(page))
            
        # elif page.route == "/forgot":
        #     page.views.clear()
        #     page.add(ft.Text("Forgot"))
            
        page.update()

    page.on_route_change = route_change
    page.go("/login")
    page.update()

ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)