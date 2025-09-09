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
    # 1. Referencia para el TextField de URL
    url_text_field = ft.TextField('', width=600, label="Introduce la URL aquí")

    # 2. Referencias para los RadioGroup de Atajos
    radio_group_indice = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value="click_izquierdo", # Valor por defecto
    )

    radio_group_corazon = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value="click_izquierdo", # Valor por defecto
    )

    radio_group_anular = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value="click_izquierdo", # Valor por defecto
    )

    radio_group_menique = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value="click_izquierdo", # Valor por defecto
    )

    radio_group_indiceDere = ft.RadioGroup(
    content=ft.Column([
        ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
        ft.Radio(value="click_derecho", label="Click Derecho"),
        ft.Radio(value="control_mouse", label="Control Mouse"),
        ft.Radio(value="click_scroll", label="Click Scroll"),
    ]),
    value="click_izquierdo", # Valor por defecto
)

    radio_group_corazon_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value="click_izquierdo", # Valor por defecto
    )

    radio_group_anular_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value="click_izquierdo", # Valor por defecto
    )

    radio_group_menique_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value="click_izquierdo", # Valor por defecto
    )
    def set_value(e):
        coefi_text.value=str(int(e.control.value))
        page.update()

    coefi_text = ft.Text("0", size=20)
    suavizadoMause=ft.CupertinoSlider(divisions=100, max=100, width=1000, on_change= set_value)
                    
                    

    def set_values(e):
        """Función que se ejecuta al hacer clic en 'Guardar' o 'Salir Sin Guardar'
           y obtiene los valores de los inputs.
        """
        url_value = url_text_field.value
        indice_shortcut = radio_group_indice.value
        corazon_shortcut = radio_group_corazon.value
        anular_shortcut = radio_group_anular.value
        menique_shortcut = radio_group_menique.value
        value=[url_value,indice_shortcut,corazon_shortcut,anular_shortcut,menique_shortcut]
        
        if(len(set(value))==len(value)):
            
                camara.setUrl(url_value)
                camara.setIzqIndice(value[1])
                camara.setIzqCorazon(value[2])
                camara.setIzqAnular(value[3])
                camara.setIzqMeñique(value[4])
                paginaAnimado.content = VistaSetinTeclado if paginaAnimado.content == paginaPrincipal else paginaPrincipal
                paginaAnimado.transition= ft.AnimatedSwitcherTransition.FADE
                page.open(ft.SnackBar(ft.Text('Seting'),bgcolor=ft.Colors.GREEN_500))
                paginaAnimado.update()

        else:
            page.open(ft.SnackBar(ft.Text('Valores Invalidos'),bgcolor=ft.Colors.RED_200))
            paginaAnimado.update()
    
    def get_radio_values():
        sencivilidad=suavizadoMause.value
        camara.setSuavisado(sencivilidad)
        """
        Obtiene los valores seleccionados de cada RadioGroup de los atajos de dedos.
        Retorna un diccionario con el dedo como clave y el valor seleccionado como valor.
        """
        # Accede al valor de cada RadioGroup usando las variables que creamos.
        indice_value = radio_group_indiceDere.value
        corazon_value = radio_group_corazon_Dere.value
        anular_value = radio_group_anular_Dere.value
        menique_value = radio_group_menique_Dere.value
        value=[indice_value,corazon_value,anular_value,menique_value]
        if(len(set(value))==len(value)):
            camara.setDereIndice(indice_value)
            camara.setDereCorazon(corazon_value)
            camara.setDereAnular(anular_value)
            camara.setDereMeñique(menique_value)
            paginaAnimado.content = VistaSetinTeclado if paginaAnimado.content == paginaPrincipal else paginaPrincipal
            paginaAnimado.transition= ft.AnimatedSwitcherTransition.FADE
            page.open(ft.SnackBar(ft.Text('Seting'),bgcolor=ft.Colors.GREEN_500))
            paginaAnimado.update()
        else:
            page.open(ft.SnackBar(ft.Text('Valores Invalidos'),bgcolor=ft.Colors.RED_200))
            paginaAnimado.update()

        


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
    
    VistaSetin = ft.Container(
        ft.Column(
            controls=[
                ft.Text('Configuración de Mouse', size=50),
                ft.Text('Suavizado de Mouse'),
                ft.Row(controls=[
                suavizadoMause,
                coefi_text 
                ]),
                ft.Text('Atajos'),

                ft.Row(controls=[
                    ft.Column(
                        [
                            ft.Text('Indice'),
                            radio_group_indiceDere, # <--- ¡Aquí usamos la variable!
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    ft.Column(
                        [
                            ft.Text('Corazón'),
                            radio_group_corazon_Dere, # <--- ¡Aquí usamos la variable!
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    ft.Column(
                        [
                            ft.Text('Anular'),
                            radio_group_anular_Dere, # <--- ¡Aquí usamos la variable!
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    ft.Column(
                        [
                            ft.Text('Meñique'),
                            radio_group_menique_Dere, # <--- ¡Aquí usamos la variable!
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    ft.Row(controls=[
                        # Asumiendo que 'seturl' es tu función para guardar o salir sin guardar
                        # y que llama a 'get_radio_values' internamente
                        ft.Button('Guardar', on_click=lambda e: print(get_radio_values())), # Ejemplo de uso
                        ft.Button('Salir Sin Guardar', on_click=lambda e: print("Salir sin guardar")) # Ejemplo
                    ]), margin=ft.margin.only(left=0, top=100, right=0, bottom=0)
                )
            ]), margin=ft.margin.only(left=50, top=100, right=50, bottom=0)
    )

    VistaSetinTeclado = ft.Container(
        ft.Column(
            controls=[
                ft.Text('Configuración de Teclado', size=50),
                ft.Text('URL'),
                url_text_field,  # Usamos la referencia al TextField
                
                ft.Text('Atajos'),

                ft.Row(
                    controls=[
                        ft.Column(
                            [
                                ft.Text('Indice'),
                                radio_group_indice, # Usamos la referencia al RadioGroup
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Column(
                            [
                                ft.Text('Corazon'),
                                radio_group_corazon, # Usamos la referencia al RadioGroup
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Column(
                            [
                                ft.Text('Anular'),
                                radio_group_anular, # Usamos la referencia al RadioGroup
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Column(
                            [
                                ft.Text('Meñique'),
                                radio_group_menique, # Usamos la referencia al RadioGroup
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(
                    ft.Row(controls=[
                        ft.ElevatedButton('Guardar', on_click=set_values), # Cambiado a ElevatedButton
                        ft.ElevatedButton('Salir Sin Guardar', on_click=seturl2), # Cambiado a ElevatedButton
                    ]),
                    margin=ft.margin.only(left=0, top=100, right=0, bottom=0)
                )
            ]
        ),
        margin=ft.margin.only(left=50, top=100, right=50, bottom=0)
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