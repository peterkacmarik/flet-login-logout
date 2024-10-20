import multiprocessing
import uvicorn
import flet as ft
from fastapi import FastAPI
from backend.api.routes.auth_route import auth_router
from frontend.views.login import LoginView
from frontend.views.register import RegisterView
from frontend.views.home import HomeView

app = FastAPI()

# Zaregistruj routery pre používateľské operácie
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

def start_flet_app():
    def main(page: ft.Page):
        page.window.always_on_top = True
        page.title = "Flet App"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = ft.padding.all(0)

        def route_change(route):
            page.views.clear()

            if page.route == "/":
                page.views.append(HomeView(page))
            elif page.route == "/login":
                page.views.append(LoginView(page))
            elif page.route == "/register":
                page.views.append(RegisterView(page))

            page.update()

        page.on_route_change = route_change
        page.go("/login")
    
    ft.app(target=main, assets_dir="frontend/assets", view=ft.AppView.FLET_APP)

def start_fastapi():
    # Spustenie FastAPI servera
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    # Vytvorenie procesov pre FastAPI a Flet
    fastapi_process = multiprocessing.Process(target=start_fastapi)
    flet_process = multiprocessing.Process(target=start_flet_app)

    # Spustenie procesov
    fastapi_process.start()
    flet_process.start()

    # Čakanie na dokončenie procesov
    fastapi_process.join()
    flet_process.join()
