import sys
import flet as ft
import UI.windouse.interfaz
if sys.platform.startswith('win'):
    print("Iniciando aplicación Flet...")
    ft.app(target=interfaz.main)
    print("La aplicación se cerró.")
elif sys.platform.startswith('linux'):
    print("Estás en Linux")
elif sys.platform == 'darwin':
    print("Estás en macOS")
else:
    print(f"Sistema operativo desconocido: {sys.platform}")