import flet as ft
from flet import Page
import threading
from detectorMano import CVMano
def main(page:Page):
    page.window.width=1200
    page.window.height=800
    page.window.resizable=False
    page.window.maximizable=False
    page.title ='Teclado y Mause Virtual'
    
    
    camara=CVMano()
    camera_feed_image = ft.Image(
        src_base64="",  # Inicialmente vacío
        fit=ft.ImageFit.CONTAIN,
        width=640,  # Ancho común para video 4:3
        height=480,  # Alto común para video 4:3
        border_radius=ft.border_radius.all(10),
        
          # Para que se vea si no hay feed
    )

    def procesarF():
        while True:
            imagen=camara.inicio2()
            camera_feed_image.src_base64=imagen
            page.update()

    def seturl(e):
        paginaAnimado.content = VistaSetin if paginaAnimado.content == paginaPrincipal else paginaPrincipal
        paginaAnimado.transition= ft.AnimatedSwitcherTransition.FADE
        page.open(ft.SnackBar(ft.Text('Seting'),bgcolor=ft.Colors.GREEN_500))
        paginaAnimado.update()
    
    def seturl2(e):
        paginaAnimado.content = VistaSetinTeclado if paginaAnimado.content == paginaPrincipal else paginaPrincipal
        paginaAnimado.transition= ft.AnimatedSwitcherTransition.FADE
        page.open(ft.SnackBar(ft.Text('Seting'),bgcolor=ft.Colors.GREEN_500))
        paginaAnimado.update()

    def handle_change(e):
        Coefi.value = str(int(e.control.value))
        page.update()

    paginaPrincipal=ft.Container(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text('Captura de Cámara', size=32),
                        ft.Container(
                            content=camera_feed_image,
                            
                            padding=10,
                            border_radius=ft.border_radius.all(10),
                            alignment=ft.alignment.center # Este ya estaba bien
                        )
                    ],
                    # horizontal_alignment en Column es su cross_axis_alignment
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centra el contenido de esta columna
                    alignment=ft.MainAxisAlignment.START, # Alinea el contenido de esta columna verticalmente al inicio
                    
                ),

                ft.Column(
                    controls=[
                        ft.Text('Opciones', size=32),
                        ft.Container(
                            content=ft.Column( # Columna interna para los botones
                                controls=[
                                    ft.ElevatedButton('URL', on_click=seturl, data=0),
                                    ft.ElevatedButton('configurar Ratón', on_click=seturl, data=1),
                                    ft.ElevatedButton('Acciones Teclado', on_click=seturl2, data=2)
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centra los botones dentro de esta columna interna
                                spacing=10
                            ),
                            # --- ¡CORRECCIÓN AQUÍ! ---
                            # alignment en ft.Container espera un ft.alignment.XYZ
                            # Esto centra el contenido (la columna de botones) DENTRO del contenedor
                            alignment=ft.alignment.center # Correcto
                        )
                    ],
                    # horizontal_alignment en Column es su cross_axis_alignment
                    horizontal_alignment=ft.CrossAxisAlignment.END, # Alinea el contenido de esta columna a la derecha
                    alignment=ft.MainAxisAlignment.START, # Alinea el contenido de esta columna verticalmente al inicio
                    
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND, # Distribuye las columnas horizontalmente
            vertical_alignment=ft.CrossAxisAlignment.START, # Alinea las columnas verticalmente al inicio (títulos a la misma altura)
            expand=True,
            
        )

    ,margin=ft.margin.only(left=50, top=90, right=50, bottom=0))
    
    VistaSetin=ft.Container(
        ft.Column(
            controls=[
                ft.Text('Configuracion de Mause',size=50),
                ft.Text('Suavizado de Mause'),
                ft.Row(controls=[
                    ft.CupertinoSlider(divisions=100, max=100,width=1000,on_change=handle_change),
                    Coefi:=ft.Text('0')
                ]),
                
                ft.Text('Atajos'),

                ft.Row(controls=[
                    ft.Column(
                        [
                            ft.Text('Indice'), # Título del dedo (Indice, Corazon, etc.)
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
                                    ft.Radio(value="click_derecho", label="Click Derecho"),
                                    ft.Radio(value="control_mouse", label="Control Mouse"),
                                    ft.Radio(value="click_scroll", label="Click Scroll"),
                                ]),
                                value="click_izquierdo", # Valor por defecto
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinea los elementos de la columna al inicio (izquierda)
                        spacing=5, # Espacio entre el título y el grupo de radios
                    ),
                    ft.Column(
                        [
                            ft.Text('Corazon'), # Título del dedo (Indice, Corazon, etc.)
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
                                    ft.Radio(value="click_derecho", label="Click Derecho"),
                                    ft.Radio(value="control_mouse", label="Control Mouse"),
                                    ft.Radio(value="click_scroll", label="Click Scroll"),
                                ]),
                                value="click_izquierdo", # Valor por defecto
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinea los elementos de la columna al inicio (izquierda)
                        spacing=5, # Espacio entre el título y el grupo de radios
                    ),
                    ft.Column(
                        [
                            ft.Text('Anular'), # Título del dedo (Indice, Corazon, etc.)
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
                                    ft.Radio(value="click_derecho", label="Click Derecho"),
                                    ft.Radio(value="control_mouse", label="Control Mouse"),
                                    ft.Radio(value="click_scroll", label="Click Scroll"),
                                ]),
                                value="click_izquierdo", # Valor por defecto
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinea los elementos de la columna al inicio (izquierda)
                        spacing=5, # Espacio entre el título y el grupo de radios
                    ),
                    ft.Column(
                        [
                            ft.Text('Meñique'), # Título del dedo (Indice, Corazon, etc.)
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
                                    ft.Radio(value="click_derecho", label="Click Derecho"),
                                    ft.Radio(value="control_mouse", label="Control Mouse"),
                                    ft.Radio(value="click_scroll", label="Click Scroll"),
                                ]),
                                value="click_izquierdo", # Valor por defecto
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinea los elementos de la columna al inicio (izquierda)
                        spacing=5, # Espacio entre el título y el grupo de radios
                    ),
                ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    ft.Row(controls=[
                        ft.Button('Guardar',on_click=seturl),
                        ft.Button('Salir Sin Guardar',on_click=seturl),
                    ]),margin=ft.margin.only(left=0, top=100, right=0, bottom=0)
                )
                ]),margin=ft.margin.only(left=50, top=100, right=50, bottom=0)

    )

    VistaSetinTeclado=ft.Container(
                ft.Column(
            controls=[
                ft.Text('Configuracion de Teclado',size=50),
                ft.Text('URL'),
                ft.TextField('',width=600),
                
                ft.Text('Atajos'),

                ft.Row(controls=[
                    ft.Column(
                        [
                            ft.Text('Indice'), # Título del dedo (Indice, Corazon, etc.)
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
                                    ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
                                    ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
                                    ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
                                ]),
                                value="click_izquierdo", # Valor por defecto
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinea los elementos de la columna al inicio (izquierda)
                        spacing=5, # Espacio entre el título y el grupo de radios
                    ),
                    ft.Column(
                        [
                            ft.Text('Corazon'), # Título del dedo (Indice, Corazon, etc.)
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
                                    ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
                                    ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
                                    ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
                                ]),
                                value="click_izquierdo", # Valor por defecto
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinea los elementos de la columna al inicio (izquierda)
                        spacing=5, # Espacio entre el título y el grupo de radios
                    ),
                    ft.Column(
                        [
                            ft.Text('Anular'), # Título del dedo (Indice, Corazon, etc.)
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
                                    ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
                                    ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
                                    ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
                                ]),
                                value="click_izquierdo", # Valor por defecto
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinea los elementos de la columna al inicio (izquierda)
                        spacing=5, # Espacio entre el título y el grupo de radios
                    ),
                    ft.Column(
                        [
                            ft.Text('Meñique'), # Título del dedo (Indice, Corazon, etc.)
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
                                    ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
                                    ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
                                    ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
                                ]),
                                value="click_izquierdo", # Valor por defecto
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinea los elementos de la columna al inicio (izquierda)
                        spacing=5, # Espacio entre el título y el grupo de radios
                    ),
                ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    ft.Row(controls=[
                        ft.Button('Guardar',on_click=lambda e:seturl(e)),
                        ft.Button('Salir Sin Guardar',on_click=seturl),
                    ]),margin=ft.margin.only(left=0, top=100, right=0, bottom=0)
                )
                ]),margin=ft.margin.only(left=50, top=100, right=50, bottom=0)

    )

    paginaAnimado=ft.AnimatedSwitcher(
        paginaPrincipal,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        
    )
    
    

    page.add(
        paginaAnimado
    )
    
    thread = threading.Thread(target=procesarF, daemon=True)
    thread.start()
ft.app(target=main)