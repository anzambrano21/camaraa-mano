
import flet as ft
import time
from flet import Page
import threading
from detectorMano import CVMano


def main(page: Page):
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = False
    page.window.maximizable = False
    page.title = 'Teclado y Mause Virtual'
    
    camara = CVMano()
    camera_feed_image = ft.Image(
        src_base64="",  # Inicialmente vacío
        fit=ft.ImageFit.CONTAIN,
        width=840,  
        height=680,  
        border_radius=ft.border_radius.all(25),
    )

    def procesarF():
        fps_objetivo = 30
        tiempo_por_fotograma = 1 / fps_objetivo
        
        while True:
            inicio_fotograma = time.time()
            
            try:
                imagen = camara.inicio2()
                camera_feed_image.src_base64 = imagen
                # Usamos page.update() o el update del control de forma segura
                camera_feed_image.update()
            except Exception as ex:
                print(f"Error en el feed de cámara: {ex}")
            
            fin_fotograma = time.time()
            tiempo_transcurrido = fin_fotograma - inicio_fotograma
            
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
        value=camara.datos['Izquierda']['indice'], 
    )

    radio_group_corazon = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value=camara.datos['Izquierda']['corazon'], 
    )

    radio_group_anular = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value=camara.datos['Izquierda']['anular'], 
    )

    radio_group_menique = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value=camara.datos['Izquierda']['menique'], 
    )

    # Radios botones de la mano derecha 
    radio_group_indiceDere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value=camara.datos['Derecha']['indice'], 
    )

    radio_group_corazon_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value=camara.datos['Derecha']['corazon'], 
    )

    radio_group_anular_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value=camara.datos['Derecha']['anular'], 
    )

    radio_group_menique_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value=camara.datos['Derecha']['menique'], 
    )
   
    coefi_text = ft.Text("0", size=20)
    
    def set_value(e):
        coefi_text.value = str(int(e.control.value))
        page.update()

    suavizadoMause = ft.CupertinoSlider(divisions=100, max=100, width=1000, on_change=set_value)
                                       
    def set_tecladoMap():
        url_value = url_text_field.value
        indice_shortcut = radio_group_indice.value
        corazon_shortcut = radio_group_corazon.value
        anular_shortcut = radio_group_anular.value
        menique_shortcut = radio_group_menique.value
        value = [indice_shortcut, corazon_shortcut, anular_shortcut, menique_shortcut]
        
        if len(set(value)) == len(value):
            camara.setUrl(url_value)
            camara.setManoIz(value)
            camara.datos['Izquierda']['indice'] = indice_shortcut
            camara.datos['Izquierda']['corazon'] = corazon_shortcut
            camara.datos['Izquierda']['anular'] = anular_shortcut
            camara.datos['Izquierda']['menique'] = menique_shortcut
            camara.guardar_datos()
            paginaAnimado.content = VistaSetinTeclado if paginaAnimado.content == paginaPrincipal else paginaPrincipal
            paginaAnimado.transition = ft.AnimatedSwitcherTransition.FADE
            page.open(ft.SnackBar(ft.Text('Configuración Guardada'), bgcolor=ft.Colors.GREEN_500))
            paginaAnimado.update()
        else:
            page.open(ft.SnackBar(ft.Text('Valores Invalidos'), bgcolor=ft.Colors.RED_200))
            paginaAnimado.update()
    
    def set_MauseMap():
        sencivilidad = suavizadoMause.value
        camara.setSuavisado(sencivilidad)
        indice_value = radio_group_indiceDere.value
        corazon_value = radio_group_corazon_Dere.value
        anular_value = radio_group_anular_Dere.value
        menique_value = radio_group_menique_Dere.value
        value = [indice_value, corazon_value, anular_value, menique_value]
        
        if len(set(value)) == len(value):
            try:
                camara.setManoDe(value)
                camara.datos['Derecha']['indice'] = indice_value
                camara.datos['Derecha']['corazon'] = corazon_value
                camara.datos['Derecha']['anular'] = anular_value
                camara.datos['Derecha']['menique'] = menique_value
                camara.guardar_datos()
                paginaAnimado.content = VistaSetinTeclado if paginaAnimado.content == paginaPrincipal else paginaPrincipal
                paginaAnimado.transition = ft.AnimatedSwitcherTransition.FADE
                page.open(ft.SnackBar(ft.Text('Configuración Guardada'), bgcolor=ft.Colors.GREEN_500))
                paginaAnimado.update()
            except Exception as e:
                print(e)
        else:
            page.open(ft.SnackBar(ft.Text('Valores Invalidos'), bgcolor=ft.Colors.RED_200))
            paginaAnimado.update()

    def SetNavegador(e):
        try:
            if paginaAnimado.content == VistaSetinTeclado:
                set_tecladoMap()
            elif paginaAnimado.content == VistaSetin:
                set_MauseMap()
        except Exception as ex:
            print(ex)
            
        index = e.control.selected_index
        if index == 0:
            paginaAnimado.content = paginaPrincipal
        elif index == 1:
            paginaAnimado.content = VistaSetinTeclado
        else:
            paginaAnimado.content = VistaSetin
            
        paginaAnimado.transition = ft.AnimatedSwitcherTransition.FADE
        page.update()
    
    def modoGame(e):
        if e.control.value:
            try:
                camara.ModoGame()
            except Exception as ex:
                print(ex)
        else:
            camara.cargar()

    # Construcción de vistas
    navegador = ft.Container(
        col=1,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    border_radius=15,
                    content=ft.NavigationRail(
                        on_change=SetNavegador,
                        height=500,
                        selected_index=0,
                        destinations=[
                            ft.NavigationRailDestination(icon=ft.Icons.HOME),
                            ft.NavigationRailDestination(icon=ft.Icons.KEYBOARD),
                            ft.NavigationRailDestination(icon=ft.Icons.MOUSE)
                        ]
                    )
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Text('Modo Game'),
                            ft.Switch(value=False, on_change=modoGame)
                        ]
                    )
                )
            ]
        )
    )

    paginaPrincipal = ft.Container(
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
                            alignment=ft.alignment.center 
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                    alignment=ft.MainAxisAlignment.START, 
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND, 
            vertical_alignment=ft.CrossAxisAlignment.START, 
            expand=True,
        )
    )
    
    VistaSetin = ft.Container(
        ft.Column(
            controls=[
                ft.Text('Configuración de Mouse', size=50),
                ft.Text('Suavizado de Mouse'),
                ft.Row(controls=[suavizadoMause, coefi_text]),
                ft.Text('Atajos'),
                ft.Row(controls=[
                    ft.Column([ft.Text('Indice'), radio_group_indiceDere], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    ft.Column([ft.Text('Corazón'), radio_group_corazon_Dere], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    ft.Column([ft.Text('Anular'), radio_group_anular_Dere], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    ft.Column([ft.Text('Meñique'), radio_group_menique_Dere], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]), margin=ft.margin.only(left=50, top=100, right=50, bottom=0)
    )

    VistaSetinTeclado = ft.Container(
        ft.Column(
            controls=[
                ft.Text('Configuración de Teclado', size=50),
                ft.Text('URL'),
                url_text_field,
                ft.Text('Atajos'),
                ft.Row(
                    controls=[
                        ft.Column([ft.Text('Indice'), radio_group_indice], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                        ft.Column([ft.Text('Corazon'), radio_group_corazon], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                        ft.Column([ft.Text('Anular'), radio_group_anular], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                        ft.Column([ft.Text('Meñique'), radio_group_menique], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ]
        ),
        margin=ft.margin.only(left=50, top=100, right=50, bottom=0)
    )

    paginaAnimado = ft.AnimatedSwitcher(
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
    
    # Iniciamos el hilo de la cámara justo antes de terminar la inicialización
    thread = threading.Thread(target=procesarF, daemon=True)
    thread.start()

# CAMBIO CLAVE: Cambiado ft.run(main) por ft.app
if __name__ == "__main__":
    print("Iniciando aplicación Flet...")
    ft.app(target=main)
    print("La aplicación se cerró.")