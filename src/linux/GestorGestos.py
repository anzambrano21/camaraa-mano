from math import sqrt
import json
import os
import time


class GestorGestos:
    def __init__(self):
        dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.dir_gestos=os.path.join(dir,"gestos_custom.json")
        self.gestos = []
    def cargar_gestos(self):
        with open(self.dir_gestos, 'r') as f:
            self.gestos = json.load(f)['gestos']
    def guardar_gesto(self,nombre,mano,dedos,distancias,accion):
        self.gestos.append({
            "nombre": nombre,
            "mano": mano,
            "dedos": dedos,
            "distancias": distancias,
            "accion": accion
        })
        with open(self.dir_gestos, 'w') as f:
            json.dump({"gestos": self.gestos})
    def eliminar_gestos(self,id):
        gestosB=self.gestos
        gestosB.pop(id)
    def detectarGestoss(self,dedos,distancias):
        pass
    
            
            

   