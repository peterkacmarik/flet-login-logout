import flet as ft



def error_field() -> ft.Text:
    return ft.Text(value="", color=ft.colors.RED)


def email_field() -> ft.TextField:
    return ft.TextField(label="Email", text_size=16, border_radius=ft.border_radius.all(10))


def password_field() -> ft.TextField:
    return ft.TextField(label="Password", text_size=16, border_radius=ft.border_radius.all(10), password=True, can_reveal_password=True)


def confirm_password_field() -> ft.TextField:
    return ft.TextField(label="Confirm Password", text_size=16, border_radius=ft.border_radius.all(10), password=True, can_reveal_password=True)