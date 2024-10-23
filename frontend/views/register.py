import flet as ft
import httpx
import time
import asyncio

from frontend.components.images import register_image
from frontend.components.fields import (
    email_field,
    password_field,
    error_field,
    confirm_password_field,
)
from frontend.components.buttons import register_button, back_to_login_button
from frontend.utils.validators import Validater
# from frontend.core.config import frontend_settings

import os
from dotenv import load_dotenv
load_dotenv()

AUTH_ENDPOINT_REGISTER = os.getenv("AUTH_ENDPOINT_REGISTER")


class RegisterView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/register")  # Správne nastavenie route
        self.page = page  # Uloženie referencie na page
        
        self.register_image = register_image()
        self.error_field = error_field()

        self.email_field = email_field()
        self.password_field = password_field()
        self.confirm_password_field = confirm_password_field()
        
        self.registration_button = register_button(self.handle_register)
        self.back_to_login_button = back_to_login_button(self.page)

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        self.register_image,
                        self.error_field,
                        self.email_field,
                        self.password_field,
                        self.confirm_password_field,
                        self.registration_button,
                        self.back_to_login_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20
                ),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
                expand=True,
            )
        ]


    def handle_register(self, e):
        email = self.email_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        # validater = Validater(page=self.page, error_field=self.error_field, email=email, password=password, confirm_password=confirm_password)
        # if not validater.is_valid():
        #     return  # Ak validácia zlyhá, nepokračuj
        
        try:
            # Volanie API pre registráciu
            response: httpx.Response = httpx.post(
                AUTH_ENDPOINT_REGISTER,
                # f"{frontend_settings.API_BASE_URL}/register", 
                json={
                    "email": email, 
                    "password": password
                }
            )

            if response.status_code == 200:
                # Registrácia úspešná, presmeruj na prihlasovaciu stránku
                self.error_field.value = "Registration successful"
                self.error_field.color = ft.colors.GREEN
                self.error_field.size = 14
                self.page.update()

                # Časový odstup na zobrazenie úspešnej správy
                # await asyncio.sleep(2)
                
                # Vymazať overlay a aktualizáciu stránky
                self.page.controls.clear()
                self.page.update()
                self.page.go("/login")

            else:
                try:
                    # Spracovanie chybových hlásení z API
                    error_message = response.json().get("detail")[0].get("msg", "Unknown error")
                except (ValueError, KeyError):
                    error_message = response.text
                self.error_field.value = error_message
                self.error_field.color = ft.colors.RED
                self.error_field.size = 14
                self.page.update()

        except Exception as ex:
            self.error_field.value = f"An error occurred during registration: {str(ex)}"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()