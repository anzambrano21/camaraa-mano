import flet as ft
import time
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
        width=840,  # Ancho común para video 4:3
        height=680,  # Alto común para video 4:3
        border_radius=ft.border_radius.all(25),
        
          # Para que se vea si no hay feed
    )

    def procesarF():
            # Establece el FPS objetivo (por ejemplo, 30 FPS es suficiente para una experiencia fluida)
        fps_objetivo = 30
        # Calcula el tiempo mínimo por fotograma en segundos
        tiempo_por_fotograma = 1 / fps_objetivo
        
        while True:
            # Marca el tiempo de inicio de este fotograma
            inicio_fotograma = time.time()
            
            imagen = camara.inicio2()
            camera_feed_image.src_base64 = imagen
            
            # Actualiza la interfaz de usuario
            page.update()
            
            # Marca el tiempo de finalización del fotograma
            fin_fotograma = time.time()
            
            # Calcula cuánto tiempo ha tardado en procesarse este fotograma
            tiempo_transcurrido = fin_fotograma - inicio_fotograma
            
            # Si el tiempo transcurrido es menor que el tiempo mínimo por fotograma,
            # espera la diferencia para mantener el FPS objetivo
            if tiempo_transcurrido < tiempo_por_fotograma:
                time.sleep(tiempo_por_fotograma - tiempo_transcurrido)
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
    coefi_text = ft.Text("0", size=20)
    
    def set_value(e):
        coefi_text.value=str(int(e.control.value))
        page.update()

    suavizadoMause=ft.CupertinoSlider(divisions=100, max=100, width=1000, on_change= set_value)
                                     
    def set_tecladoMap(e):
        """Función que se ejecuta al hacer clic en 'Guardar' o 'Salir Sin Guardar'
           y obtiene los valores de los inputs.
        """
        url_value = url_text_field.value
        indice_shortcut = radio_group_indice.value
        corazon_shortcut = radio_group_corazon.value
        anular_shortcut = radio_group_anular.value
        menique_shortcut = radio_group_menique.value
        value=[indice_shortcut,corazon_shortcut,anular_shortcut,menique_shortcut]
        
        if(len(set(value))==len(value)):
            
                camara.setUrl(url_value)
                camara.setManoIz(value)
                camara.datos['Izquierda']['indice']=indice_shortcut
                camara.datos['Izquierda']['corazon']=corazon_shortcut
                camara.datos['Izquierda']['anular']=anular_shortcut
                camara.datos['Izquierda']['menique']=menique_shortcut
                camara.guardar_datos()
                paginaAnimado.content = VistaSetinTeclado if paginaAnimado.content == paginaPrincipal else paginaPrincipal
                paginaAnimado.transition= ft.AnimatedSwitcherTransition.FADE
                page.open(ft.SnackBar(ft.Text('Seting'),bgcolor=ft.Colors.GREEN_500))
                paginaAnimado.update()

        else:
            page.open(ft.SnackBar(ft.Text('Valores Invalidos'),bgcolor=ft.Colors.RED_200))
            paginaAnimado.update()
    
    def set_MauseMap():
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

            try:
                camara.setManoDe(value)
                camara.datos['Derecha']['indice']=indice_value
                camara.datos['Derecha']['corazon']=corazon_value
                camara.datos['Derecha']['anular']=anular_value
                camara.datos['Derecha']['menique']=menique_value
                camara.guardar_datos()
                paginaAnimado.content = VistaSetinTeclado if paginaAnimado.content == paginaPrincipal else paginaPrincipal
                paginaAnimado.transition= ft.AnimatedSwitcherTransition.FADE
                page.open(ft.SnackBar(ft.Text('Seting'),bgcolor=ft.Colors.GREEN_500))
                paginaAnimado.update()
            except Exception as e:
                print(e)
            
        else:
            page.open(ft.SnackBar(ft.Text('Valores Invalidos'),bgcolor=ft.Colors.RED_200))
            paginaAnimado.update()

    

    def SetNavegador(e):
        index=e.control.selected_index
        print(index)
        if(index==0 ):
            paginaAnimado.content=paginaPrincipal
        elif(index==1):
            paginaAnimado.content=VistaSetinTeclado
        else:
            paginaAnimado.content=VistaSetin
        paginaAnimado.transition= ft.AnimatedSwitcherTransition.FADE
        page.open(ft.SnackBar(ft.Text('Seting'),bgcolor=ft.Colors.GREEN_500))
        paginaAnimado.update()
    
    
    navegador= ft.Container(
        
        
        col=1,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    border_radius=15,
                    content=ft.NavigationRail(
                        on_change=SetNavegador,
                        height=500,
                        
                        bgcolor=ft.Colors.AMBER,
                        selected_index=0,
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.Icons.HOME
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.KEYBOARD
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.MOUSE
                            )
                        ]
                    )
            )
            ]
        )
    )


    paginaPrincipal=ft.Container(
        
        
        content=ft.Row(
            
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text('Captura de Cámara', size=32),
                            ft.Container(
                                expand=True,
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


                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND, # Distribuye las columnas horizontalmente
                vertical_alignment=ft.CrossAxisAlignment.START, # Alinea las columnas verticalmente al inicio (títulos a la misma altura)
                expand=True,
                
            )

    ,#margin=ft.margin.only(left=50, top=90, right=50, bottom=0)
    )
    

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
                        # y que llama a 'set_MauseMap' internamente
                        ft.Button('Guardar', on_click=lambda e: print(set_MauseMap())), # Ejemplo de uso
                        
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
                        ft.ElevatedButton('Guardar', on_click=set_tecladoMap), # Cambiado a ElevatedButton
                         # Cambiado a ElevatedButton
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
        expand=True,
        
    )
    
    page.add(
        ft.Row(
            expand=True,
            controls=[
                navegador,
                paginaAnimado
            ]
        )
        
    )
    
    thread = threading.Thread(target=procesarF, daemon=True)
    thread.start()
ft.app(target=main)