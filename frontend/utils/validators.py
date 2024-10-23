import re
import flet as ft
import requests
import time


class Validater:
    def __init__(self, page: ft.Page, error_field: ft.Text, email: ft.TextField, password: ft.TextField, confirm_password: ft.TextField=None):
        self.page = page
        self.error_field = error_field
        self.email = email
        self.password = password
        self.confirm_password = confirm_password


    def validate_login_fields(self):
        if not self.email or not self.password:
            # self.error_field.visible = True
            self.error_field.value = "Please fill in all fields"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            # self.page.update()
            return False
        return True


    def validate_email(self):
        pattern: str = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        result: bool = re.match(pattern, self.email)
        if not result:
            self.error_field.visible = True
            self.error_field.value = "Please enter a valid email address"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()
            return False
        return True


    def validate_password(self):
        if self.password != self.confirm_password:
            self.error_field.visible = True
            self.error_field.value = "Passwords do not match"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()
            return False
        
        if len(self.password) < 8:
            self.error_field.visible = True
            self.error_field.value = "Password must be at least 8 characters long"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()
            return False
        
        if not any(char.isdigit() for char in self.password):
            self.error_field.visible = True
            self.error_field.value = "Password must contain at least one number"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()
            return False
        
        if not any(char.isupper() for char in self.password):
            self.error_field.visible = True
            self.error_field.value = "Password must contain at least one uppercase letter"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()
            return False
        
        if not any(char.islower() for char in self.password):
            self.error_field.visible = True
            self.error_field.value = "Password must contain at least one lowercase letter"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()
            return False
        return True


    def validate_register_response(self, response: requests.Response):
        if response.status_code == 200:
            self.error_field.visible = True
            self.error_field.value = "Registration successful"
            self.error_field.color = ft.colors.GREEN
            self.error_field.size = 14
            self.page.update()

            time.sleep(2)
            self.page.overlay.clear()
            self.page.update()
            self.page.go("/login")
            return True

        elif response.status_code == 401:
            self.error_field.visible = True
            self.error_field.value = "Invalid email or password"
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()
            return False
        
        else:
            error_msg = response.json().get("detail", [{"msg": "Unknown error"}])[0].get("msg")
            self.error_field.visible = True
            self.error_field.value = error_msg
            self.error_field.color = ft.colors.RED
            self.error_field.size = 14
            self.page.update()
            return False







