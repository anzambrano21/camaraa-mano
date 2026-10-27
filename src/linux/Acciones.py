from pynput.keyboard import Key, Controller as KBController
from pynput.mouse import Button, Controller as MouseController
import time

class Acciones:
    def __init__(self):
        self.keyboard=KBController()
        self.mouse=MouseController()
        
    def ejecutaar(self,Accion):
        pass
    def ejecutar_Tecla(self):
        pass
    def ejecutarCombo(self):
        pass
    def ejecutar_click(self):
        pass
    def ejecutar_scroll(self):
        pass
        