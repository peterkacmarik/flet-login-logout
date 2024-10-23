import flet as ft
import requests
import time
import httpx

from frontend.components.buttons import (
    login_button, 
    create_account_button, 
    forgot_password_button,
)
from frontend.components.fields import (
    email_field,
    password_field,
    error_field
)
from frontend.components.images import login_image
from frontend.components.checkbox import remember_me_checkbox
from frontend.utils.validators import Validater
# from frontend.core.config import frontend_settings

import os
from dotenv import load_dotenv
load_dotenv()

AUTH_ENDPOINT_LOGIN = os.getenv("AUTH_ENDPOINT_LOGIN")


class LoginView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/login")
        self.page = page
        
        self.login_image = login_image()
        self.error_field = error_field()
        self.email_field = email_field()
        self.password_field = password_field()
        
        # Checkbox na zapamätanie prihlásenia
        self.remember_me_checkbox  = remember_me_checkbox()
        
        self.login_button = login_button(self.handle_login)
        self.create_account_button = create_account_button(self.page)
        self.forgot_password_button = forgot_password_button(self.page)
        
        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        self.login_image,
                        self.error_field,
                        self.email_field,
                        self.password_field,
                        self.remember_me_checkbox,
                        self.login_button,
                        self.create_account_button,
                        self.forgot_password_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20
                ),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
        
        self.load_email_if_saved()
        
        
    def handle_login(self, e):
        email = self.email_field.value
        password = self.password_field.value

        validater = Validater(page=self.page, error_field=self.error_field, email=email, password=password)
        
        # validater.validate_login_fields()
        # validater.validate_email()
        # validater.validate_password()
        
        # Uloženie emailu do uloženého prostredia
        if self.remember_me_checkbox.value:
            self.page.client_storage.set("user_email", email)
        else:
            self.page.client_storage.remove("user_email")
        
        try:
            # Volanie API pre prihlasovanie
            response = httpx.post(
                AUTH_ENDPOINT_LOGIN,
                # f"{frontend_settings.API_BASE_URL}/login", 
                json={
                    "email": email, 
                    "password": password
                }
            )
            
            if response.status_code == 200:                
                # Prihlasovanie úspešne, presmeruj na hlavné stránku
                self.error_field.value = "Login successful"
                self.error_field.color = ft.colors.GREEN
                self.error_field.size = 14
                self.page.update()
                
                # Časový odstup na zobrazenie úspešnej správy
                # await asyncio.sleep(2)
                
                # Vymazanie overlay a aktualizácia stránky
                self.page.controls.clear()
                self.page.update()
                self.page.go("/")
                
            elif response.status_code == 401:
                # Nesprávne prihlasovacie údaje
                self.error_field.value = "Invalid email or password"
                self.error_field.color = ft.colors.RED
                self.error_field.size = 14
                self.page.update()
            
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
            
            
    def load_email_if_saved(self):
        saved_email = self.page.client_storage.get("user_email")
        if saved_email:
            self.email_field.value = saved_email
            self.page.update()