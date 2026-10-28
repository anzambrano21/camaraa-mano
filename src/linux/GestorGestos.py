from math import sqrt
import json
import os
import time


class GestorGestos:
    def __init__(self):
        dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.dir_gestos=os.path.join(dir,"gestos_custom.json")
        self.dir_modos=os.path.join(dir,"Comando.json")
        self.gestos = []
        self.modos={}
        self.cargar_gestos()
        self.cargar_modos()
    def cargar_gestos(self):
        with open(self.dir_gestos, 'r') as f:
            self.gestos = json.load(f)['gestos']
    def cargar_modos(self):
        with open(self.dir_modos, 'r') as f:
            self.modos = json.load(f)
    def guardar_gesto(self,nombre,mano,dedos,distancias,accion):
        self.gestos.append({
            "id": f"{nombre}-{int(time.time())}",
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
    def _dedos_extendidos(self,landmarks, mano):
        dedos=[]
        dedos.append(self._distancia(landmarks[4], landmarks[0]) > self._distancia(landmarks[3], landmarks[0]))
        tip=[8,12,16,20]
        pip=[6,10,14,18]
        for i in range(4):
            dedos.append(landmarks[tip[i]][1] < landmarks[pip[i]][1])
        return dedos
    def _normalizar(self, landmarks):
        muñeca = landmarks[0]
        relativos = [(x - muñeca[0], y - muñeca[1]) for x, y in landmarks]
        ref = self._distancia(relativos[9], (0, 0))
        if ref == 0:
            return relativos
        return [(x / ref, y / ref) for x, y in relativos]
    def detectarGestoss(self, landmarks, mano):
        dedos_actual = self._dedos_extendidos(landmarks,mano)
        norm = self._normalizar(landmarks)

        for gesto in self.gestos:
            # Filtrar por mano
            if gesto["mano"] != "Any" and gesto["mano"] != mano:
                continue
            # Comparar dedos
            if dedos_actual != gesto["dedos"]:
                continue
            # Comparar distancias opcionales
            match = True
            for par, restriccion in gesto.get("distancias", {}).items():
                a, b = map(int, par.split("-"))
                dist = self._distancia(norm[a], norm[b])
                if "max" in restriccion and dist > restriccion["max"]:
                    match = False
                    break
            if match:
                return gesto
        return None

    def _distancia(self,p1,p2):
        return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

    
            
            

   