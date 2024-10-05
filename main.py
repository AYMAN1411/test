import flet as ft
from manage_sql import POSTGRESQL
from manage_sql import *

# Database connection details
url = 'postgresql://8s6d5t:xau_iSi58LvZL52Zy9NvpvoDLpulsaj4nCDB9@us-east-1.sql.xata.sh/testdatbase:main?sslmode=require'

def main(page: ft.Page):
    page.title = "Like/Dislike App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Connect to PostgreSQL database using manage-sql
    db = db=POSTGRESQL(
    postgre_url=url
)
    conn, cursor = db.conectarBanco()

    # Create table if not exists
    db.criarTabela(
        nomeTabela='like_dislike',
        Colunas=['name', 'opinion'],
        ColunasTipo=['TEXT', 'TEXT']
    )

    # Variable to store the current opinion
    current_opinion = None

    def save_opinion(e):
        name = name_input.value
        if not name:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter your name"))
            page.snack_bar.open = True
            page.update()
            return
        
        if current_opinion is None:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please select an opinion"))
            page.snack_bar.open = True
            page.update()
            return
        # db.inserirDados(nomeTabela=nometabeta, Colunas=colunas, dados=['Web Tech','webtechmoz',db.encriptarValor('1'),'ayman@gmail.com'])
        db.inserirDados(
            nomeTabela='like_dislike',
            Colunas=['name', 'opinion'],
            dados=[name, "Like" if current_opinion else "Dislike"]
        )
        update_list()
        name_input.value = ""
        reset_buttons()
        page.update()

    def update_list():
        # rows = db.verDados(
        #     nomeTabela='like_dislike',
        #     Colunas=['name', 'opinion']
        # )
        # opinions_list.controls.clear()
        # for row in rows:
        #     opinions_list.controls.append(ft.Text(f"{row[0]}: {row[1]}"))
        # page.update()
        ...

    def toggle_thumb(button: ft.IconButton, value: bool):
        nonlocal current_opinion
        current_opinion = value
        thumb_up_button.icon_color = ft.colors.BLUE if button == thumb_up_button else ft.colors.GREY
        thumb_down_button.icon_color = ft.colors.BLUE if button == thumb_down_button else ft.colors.GREY
        page.update()

    def reset_buttons():
        nonlocal current_opinion
        current_opinion = None
        thumb_up_button.icon_color = ft.colors.GREY
        thumb_down_button.icon_color = ft.colors.GREY

    name_input = ft.TextField(label="Enter your name")

    thumb_up_button = ft.IconButton(
        icon=ft.icons.THUMB_UP,
        icon_color=ft.colors.GREY,
        on_click=lambda _: toggle_thumb(thumb_up_button, True)
    )

    thumb_down_button = ft.IconButton(
        icon=ft.icons.THUMB_DOWN,
        icon_color=ft.colors.GREY,
        on_click=lambda _: toggle_thumb(thumb_down_button, False)
    )

    opinions_list = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True
    )

    page.add(
        ft.Column(
            [
                name_input,
                ft.Row(
                    [thumb_up_button, thumb_down_button],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.ElevatedButton("Save Opinion", on_click=save_opinion),
                ft.Text("Opinions:"),
                ft.Container(
                    content=opinions_list,
                    height=200,
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=5,
                    padding=10,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    update_list()

ft.app(target=main)