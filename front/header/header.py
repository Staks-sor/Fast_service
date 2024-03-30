import json
import time
import flet as ft
from flet import View, Page, AppBar, ElevatedButton, Text
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment
import requests
from flet_core import TextAlign


def main(page: ft.Page):
    # Устанавливаем заголовок страницы
    page.title = "Главная"

    # Функция для создания модальных окон
    def modal_window():
        # Окно для регистрации
        dlg_reg_user = ft.AlertDialog(
            adaptive=True,
            title=ft.Text("Регистрация", text_align="center"),
            actions=[
                ft.TextField(label="Имя", autofocus=True, col=10, scale=0.9),
                ft.TextField(label="Email", scale=0.9),
                ft.TextField(label="Пароль", password=True, scale=0.9),
                ft.OutlinedButton(
                    content=ft.Text("Регистрация"),
                    on_click=lambda e: registrator(e, dlg_reg_user),
                    scale=0.9
                )
            ]
        )
        # Окно для входа
        dlg_enter_user = ft.AlertDialog(
            adaptive=True,
            title=ft.Text("Вход", text_align="center"),
            actions=[
                ft.TextField(hint_text="Email", autofocus=True, col=10, scale=0.9),
                ft.TextField(hint_text="Пароль", password=True, scale=0.9),
                ft.CupertinoActionSheetAction(content=ft.Text("Вход")),
            ]
        )
        return dlg_reg_user, dlg_enter_user

    # Функция для открытия диалогового окна
    def open_dialog(dialog):
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Функция для регистрации пользователя
    def registrator(e, dlg_reg_user):
        name = dlg_reg_user.actions[0].value
        email = dlg_reg_user.actions[1].value
        password = dlg_reg_user.actions[2].value
        url = "http://127.0.0.1:8000/auth/register"
        data = {
            "name": name,
            "email": email,
            "password": password
        }
        response = requests.post(url, json=data)
        response_json = response.json()
        if response.status_code == 200:
            # Успешная регистрация
            dlg_success_registration = ft.AlertDialog(
                adaptive=True,
                title=ft.Text("Вы успешно зарегистрированы", text_align="center")
            )
            open_dialog(dlg_success_registration)
            time.sleep(1)
            dlg_success_registration.open = False
            page.update()
        else:
            # Ошибка при регистрации
            error_description = response_json['detail'][0]['msg']
            dlg_error_registration = ft.AlertDialog(
                adaptive=True,
                title=ft.Text(error_description, text_align="center")
            )
            open_dialog(dlg_error_registration)
            time.sleep(2)
            open_dialog(dlg_reg_user)
            print("Ошибка при регистрации пользователя:", response.text)

    # Функция для изменения маршрута
    def route_change(e: RouteChangeEvent) -> None:
        # Создаем модальные окна
        dlg_reg_user, dlg_enter_user = modal_window()
        # Очищаем предыдущие представления
        page.views.clear()
        # Добавляем новое представление
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    # Футер
                    ft.BottomAppBar(
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        shape=ft.NotchShape.CIRCULAR,
                        height=45,
                        content=Text("this is footer", size=10, text_align=TextAlign.CENTER)
                    ),
                    # Верхняя панель приложения
                    ft.AppBar(
                        title=ft.Text("Автосервис"),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        actions=[
                            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                            # Кнопка "Регистрация"
                            ft.OutlinedButton(
                                content=ft.Text("Регистрация"),
                                on_click=lambda e: open_dialog(dlg_reg_user),
                                scale=0.9
                            ),
                            # Кнопка "Вход"
                            ft.OutlinedButton(
                                content=ft.Text("Вход"),
                                on_click=lambda e: open_dialog(dlg_enter_user),
                                scale=0.9
                            )
                        ],
                    ),
                ],
            )
        )
        page.update()

    # Функция для удаления представления из стека
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Привязываем функции к событиям
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
