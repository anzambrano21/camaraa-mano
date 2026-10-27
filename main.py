import sys
import flet as ft
if sys.platform.startswith('win'):
    print("Iniciando aplicación Flet...")
    from UI.windouse.interfaz import main
    ft.app(target=main)
    print("La aplicación se cerró.")
elif sys.platform.startswith('linux'):
    print("Estás en Linux")
    from UI.linux.interfaz import main
    ft.run(main)

