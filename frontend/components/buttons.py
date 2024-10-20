import flet as ft



def login_button(handle_login):
    return ft.ElevatedButton("Login", on_click=handle_login)


def create_account_button(page: ft.Page):
    return ft.TextButton("Create Account", on_click=lambda _: page.go("/register"), visible=True)


def forgot_password_button(page: ft.Page):
    return ft.TextButton("Forgot Password?", on_click=lambda _: page.go("/forgot_password"), visible=False)


def register_button(handle_register):
    return ft.ElevatedButton("Register", on_click=handle_register)

def back_to_login_button(page: ft.Page):
    return ft.TextButton("Back to Login", on_click=lambda _: page.go("/login"))