import flet as ft

def main(page: ft.Page):

    # Configuración de la ventana principal
    page.title = "Teclado y Mouse Virtual"
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = False
    page.window.maximizable = False
    

    #componentes
    Imagen=ft.Image(
        src="",
        width=640,
        height=480,
        border_radius=25,
        )

    vistaPrincipal = ft.Container(
        padding=10,
        content=ft.Row( controls=[
            ft.Column(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.MOUSE,
                    on_click=lambda e: print("Boton presionado"),
                    icon_color="white"
                ),
                ft.IconButton(
                    icon=ft.Icons.KEYBOARD,
                    on_click=lambda e: print("Boton presionado"),
                    icon_color="white"
                )
            ]
        ),
        Imagen
        ])
    )
    page.add(vistaPrincipal)
    


