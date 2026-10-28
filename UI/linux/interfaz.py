import time
import flet as ft
from src.linux.DetectarMano import CVMano
import asyncio

def main(page: ft.Page):

    # Configuración de la ventana principal
    page.title = "Teclado y Mouse Virtual"
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = False
    page.window.maximizable = False
    
    Detector = CVMano()

    # Componentes


    #definicion de la imagen
    camera_feed_image = ft.Image(
        src="",  
        width=840,  
        height=680,  
        border_radius=25,
        gapless_playback=True
    )
    
    running = True
    Actualizacion=True

    #definicion de funcion receptor de imagen para interfaz 
    async def procesar_feed():
        nonlocal Actualizacion
        fps_objetivo = 30
        tiempo_por_frame = 1 / fps_objetivo
        while running:
            inicio = time.time()
            if not Actualizacion:
                await asyncio.sleep(1)
                continue
            try:
                frame_b64 = await asyncio.to_thread(Detector.get_Frame)
                if frame_b64 and Actualizacion:
                    camera_feed_image.src = frame_b64
                    camera_feed_image.update()
            except Exception as ex:
                print(f"Error en feed de cámara: {ex}")
                break

            transcurrido = time.time() - inicio
            if transcurrido < tiempo_por_frame:
                await asyncio.sleep(tiempo_por_frame - transcurrido)
            else:
                await asyncio.sleep(0.03)

    # Iniciar la captura de video en segundo plano
    page.run_task(procesar_feed)
    
    #definicion de evento de cierre de ventana para liberacion de hilos de forma segura 
    async def on_window_event(e):
        nonlocal running
        if e.data == "close":
            running = False
            Detector.liberar()
            page.window.destroy()

    
    page.window.on_event = on_window_event


    def SetNavegador(e):
        nonlocal Actualizacion

        index = e.control.selected_index
        if index == 0:
            paginaAnimado.content = paginaPrincipal
            Actualizacion=True
        elif index == 1:
            paginaAnimado.content = VistaSetinTeclado
            Actualizacion=False
        elif index == 2:
            paginaAnimado.content = VistaSetin
            Actualizacion=False
        elif index == 3:
            paginaAnimado.content = VistaSetinGestos
            Actualizacion=False
            
        paginaAnimado.transition = ft.AnimatedSwitcherTransition.FADE
        page.update()

     
    def modoGame(e):
        pass
    def setsenci(e):
        coefi_text.value = str(e.control.value)
        coefi_text.update()
    
    def capturar_gesto(e):
        mano = mano_selector.value
        landmarks = Detector.obtener_landmarks(mano)
        if landmarks is None:
            # Mostrar SnackBar de error: "No se detecta la mano"
            return
        
        nombre = nombre_gesto_field.value
        accion = {
            "tipo": tipo_accion_dropdown.value,
            "valor": valor_accion_field.value  # parsear si es combo: "ctrl+c" → ["ctrl", "c"]
        }
        
        Detector.gestor.registrar_gesto(nombre, mano, landmarks, accion)
    # Actualizar lista, mostrar SnackBar de éxito, limpiar campos

    """
    Definicion de de componentes de la interfaz (flet) 
    dedicado exclusivamente para crear componentes de la interfaz   
       
    """

    #crear vista para la gestion de gestos 
    def crear_lista_gestos():
        """Genera la lista de gestos guardados con botón eliminar"""
        items = []
        for gesto in Detector.gestor.gestos:
            items.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.GESTURE),
                    title=ft.Text(gesto["nombre"]),
                    subtitle=ft.Text(f"Mano: {gesto['mano']} | {gesto['accion']['tipo']}: {gesto['accion']['valor']}"),
                    trailing=ft.IconButton(
                        ft.Icons.DELETE,
                        on_click=lambda e, gid=gesto["id"]: eliminar_gesto(gid)
                    ),
                )
            )
        return items

    def eliminar_gesto(gesto_id):
        Detector.gestor.eliminar_gesto(gesto_id)
        lista_gestos_column.controls = crear_lista_gestos()
        page.update()

    nombre_gesto_field = ft.TextField(label="Nombre del gesto")
    mano_selector = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Left", label="Izquierda"),
            ft.Radio(value="Right", label="Derecha"),
            ft.Radio(value="Any", label="Cualquiera"),
        ]),
        value="Left"
    )
    tipo_accion_dropdown = ft.Dropdown(
        label="Tipo de acción",
        options=[
            ft.dropdown.Option("tecla", "Tecla"),
            ft.dropdown.Option("tecla_combo", "Combinación de teclas"),
            ft.dropdown.Option("mouse_click", "Click de mouse"),
            ft.dropdown.Option("mouse_scroll", "Scroll"),
        ]
    )
    valor_accion_field = ft.TextField(label="Valor (ej: a, ctrl+c, click_izquierdo)")

    lista_gestos_column = ft.Column(controls=crear_lista_gestos())

    VistaSetinGestos = ft.Container(
        ft.Column(
            controls=[
                ft.Text('Gestión de Gestos', size=50),
                ft.Divider(),
                ft.Text('Gestos guardados', size=20),
                lista_gestos_column,
                ft.Divider(),
                ft.Text('Crear nuevo gesto', size=20),
                nombre_gesto_field,
                mano_selector,
                tipo_accion_dropdown,
                valor_accion_field,
                ft.Button("🔴 Capturar y Guardar", on_click=capturar_gesto),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        margin=ft.margin.Margin.only(left=50, top=50, right=50, bottom=0),
        expand=True,
    )




    
    navegador = ft.Container(
        width=200, 
        padding=10,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    border_radius=15, 
                    height=500,
                    content=ft.NavigationRail(
                        on_change=SetNavegador,
                        selected_index=0,
                        destinations=[
                            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Home"),
                            ft.NavigationRailDestination(icon=ft.Icons.KEYBOARD, label="Set Keyboard"),
                            ft.NavigationRailDestination(icon=ft.Icons.MOUSE, label="Set Mouse"),
                            ft.NavigationRailDestination(icon=ft.Icons.GESTURE, label="Gestos")
                        ]
                    )
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.TRANSPARENT,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text('Modo Game', size=12, color=ft.Colors.WHITE),
                            ft.Switch(value=False, on_change=modoGame)
                        ]
                    )
                )
            ]
        )
    )
    
    paginaPrincipal = ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text('Captura de Cámara', size=28, weight="bold"),
                ft.Container(
                    content=camera_feed_image,
                    padding=10,
                    border_radius=10,
                    alignment=ft.alignment.Alignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            alignment=ft.MainAxisAlignment.START, 
        )
    )
    
    #pagina de configuracion


    #Componentes de la pagina de configuraciomn mano izquierda
    url_text_field = ft.TextField('', width=600, label="Introduce la URL aquí")

    # 2. Referencias para los RadioGroup de Atajos
    radio_group_indice = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value=Detector.datos['Izquierda']['indice'], 
    )

    radio_group_corazon = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value=Detector.datos['Izquierda']['corazon'], 
    )

    radio_group_anular = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value=Detector.datos['Izquierda']['anular'], 
    )

    radio_group_menique = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="ctrl+Tap", label="Segunda Ventana"),
            ft.Radio(value="ctrl+Tap3", label="Tercera Ventana"),
            ft.Radio(value="ctrl+Tap4", label="Cuarta Ventana"),
            ft.Radio(value="ctrl+Tap5", label="Quinta Ventana"),
        ]),
        value=Detector.datos['Izquierda']['menique'], 
    )

    # Radios botones de la mano derecha 
    radio_group_indiceDere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value=Detector.datos['Derecha']['indice'], 
    )

    radio_group_corazon_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value=Detector.datos['Derecha']['corazon'], 
    )

    radio_group_anular_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value=Detector.datos['Derecha']['anular'], 
    )

    radio_group_menique_Dere = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="click_izquierdo", label="Click Izquierdo"),
            ft.Radio(value="click_derecho", label="Click Derecho"),
            ft.Radio(value="control_mouse", label="Control Mouse"),
            ft.Radio(value="click_scroll", label="Click Scroll"),
        ]),
        value=Detector.datos['Derecha']['menique'], 
    )
   
    coefi_text = ft.Text("0", size=20)
    suavizadoMause = ft.CupertinoSlider(divisions=100, max=100, width=1000, on_change=setsenci)

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
        margin=ft.margin.Margin.only(left=50, top=100, right=50, bottom=0)
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
            ]), margin=ft.margin.Margin.only(left=50, top=100, right=50, bottom=0)
    )

    #definicion de pagina animada
    paginaAnimado = ft.AnimatedSwitcher(
        paginaPrincipal,
        transition="scale",
        duration=500,
        reverse_duration=100,
        switch_in_curve="bounce_out",
        switch_out_curve="bounce_in",
        expand=True,
    )
    # Estructura principal dividida en dos columnas ordenadas
    page.add(
        ft.Row(
            controls=[
                navegador, 
                ft.VerticalDivider(width=1), # Una línea divisoria elegante
                paginaAnimado
            ], 
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )

