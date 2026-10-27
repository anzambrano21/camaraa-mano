from pynput.keyboard import Key, Controller as KBController
from pynput.mouse import Button, Controller as MouseController
import time

class Acciones:
    def __init__(self):
        self.keyboard=KBController()
        self.mouse=MouseController()
        
    def ejecutar(self,Accion):
        if Accion["tipo"] == "tecla":
            self.ejecutar_Tecla(Accion["valor"])
        elif Accion["tipo"] == "combo":
            self.ejecutarCombo(Accion["valor"])
        elif Accion["tipo"] == "click":
            self.ejecutar_click()
        elif Accion["tipo"] == "scroll":
            self.ejecutar_scroll(Accion["valor"])
    def ejecutar_Tecla(self,tecla):
        self.keyboard.press(tecla)
        self.keyboard.release(tecla)
        time.sleep(0.1)
    def ejecutarCombo(self,teclas):
        for tecla in teclas:
            self.keyboard.press(tecla)
        for tecla in teclas:
            self.keyboard.release(tecla)
        time.sleep(0.1)
    def ejecutar_click(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        time.sleep(0.1)
    def ejecutar_scroll(self,direccion):
        self.mouse.scroll(0, 6*direccion)
        time.sleep(0.1)
        