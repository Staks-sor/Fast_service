import flet as ft
import logging

logging.basicConfig(level=logging.DEBUG)


def main(page: ft.Page):
    page.title = "Главная"
    first_name = ft.Ref[ft.TextField]()
    last_name = ft.Ref[ft.TextField]()
    dlg_reg_user = ft.AlertDialog(adaptive=True,
                                  title=ft.Text("Регистрация", text_align="center"),

                                  actions=[
                                      ft.TextField(hint_text="email", autofocus=True, col=10, scale=0.9, ),
                                      ft.TextField(hint_text="Телефон", scale=0.9),
                                      ft.TextField(hint_text="Пароль", password=True, scale=0.9),

                                      ft.CupertinoActionSheetAction(
                                          content=ft.Text("Зарегестрироваться")),
                                  ]
                                  )

    print(ft.Text(f"{first_name.current.value}"))
    dlg_enter_user = ft.AlertDialog(adaptive=True,
                                    title=ft.Text("Вход", text_align="center"),
                                    actions=[
                                        ft.TextField(hint_text="email", autofocus=True, col=10, scale=0.9),
                                        ft.TextField(hint_text="Пароль", password=True, scale=0.9),

                                        ft.CupertinoActionSheetAction(
                                            content=ft.Text("Вход")),
                                    ]
                                    )

    def open_reg(e):
        page.dialog = dlg_reg_user
        dlg_reg_user.open = True
        page.update()

    def open_enter_user(e):
        page.dialog = dlg_enter_user
        dlg_enter_user.open = True
        page.update()

    def route_change(route, login_function=None, registration_function=None, check_item_clicked=None):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text("Автосервис"),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        actions=[
                            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                            ft.OutlinedButton(content=ft.Text("Регистрация"), on_click=open_reg, scale=0.9),
                            ft.OutlinedButton(content=ft.Text("Вход"), on_click=open_enter_user, scale=0.9)
                        ],

                    ),
                ],
            )
        )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
