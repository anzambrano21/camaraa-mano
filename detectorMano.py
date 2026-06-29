import os
import sys
import time
import math
import json
import base64
import threading
import webbrowser
import cv2
import mediapipe as mp
import pyautogui
import pydirectinput
from ctypes import cast, POINTER
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
from mano import Mano

# -------------------------------------------------------------------------
# ADAPTADORES DE COMPATIBILIDAD (Para no romper la lógica existente)
# -------------------------------------------------------------------------
class LandmarkWrapper:
    def __init__(self, landmarks):
        self.landmark = landmarks

class ClassificationWrapper:
    def __init__(self, label):
        self.label = label

class HandednessWrapper:
    def __init__(self, label):
        self.classification = [ClassificationWrapper(label)]
# -------------------------------------------------------------------------

class CVMano:

    def __init__(self):
        self.datos = {}

        self.atajosManos = {
            'click_izquierdo': pyautogui.click,
            'control_mouse': self.__moverMouseSuavizado,
            'click_derecho': pyautogui.rightClick,
            'click_scroll': self.Scroll,
            'ctrl+Tap': lambda: self.__press_alt_tab(0.5, 1),
            'ctrl+Tap3': lambda: self.__press_alt_tab(0.5, 2),
            'ctrl+Tap4': lambda: self.__press_alt_tab(0.5, 3),
            'ctrl+Tap5': lambda: self.__press_alt_tab(0.5, 4),
        }
        
        # CORREGIDO: Corrección de typo 'meniqie' -> 'menique' y 'mause' -> 'mouse'
        self.modoGames = {
            'indice': lambda: self.precionarTecla(1, 'd'),
            'corazon': lambda: self.precionarTecla(1, 'w'),
            'anular': lambda: self.precionarTecla(1, 'a'),
            'menique': lambda: self.precionarTecla(1, 'shift'), 
            'mouse': self.__movermouseV2
        }

        self.cargar()
        self.__URL_PRINCIPAL = 'https://www.youtube.com/watch?v=44pt8w67S8I'
        self.__camara = cv2.VideoCapture(0)
       
        # -----------------------------------------------------------------
        # CONFIGURACIÓN: MediaPipe Tasks API
        # -----------------------------------------------------------------
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.resource_path('hand_landmarker.task')),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.__manos = HandLandmarker.create_from_options(options)
        
        self.__HAND_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 4),        # Pulgar
            (0, 5), (5, 6), (6, 7), (7, 8),        # Índice
            (5, 9), (9, 10), (10, 11), (11, 12),   # Corazón
            (9, 13), (13, 14), (14, 15), (15, 16), # Anular
            (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Meñique y Palma
        ]
        # -----------------------------------------------------------------

        self.__enlace_principal_abierto = False
        self.__dedos_cerrados_estado = []
        self.__ventana_suavizado = 5
        self.pubix, self.pubiy = 0, 0
        self.__anchopanta, self.__altopanta = pyautogui.size()
        self.tX = 0
        self.tY = 0
        self.x, self.y = 0, 0
 
        self.CVMano = None
        self.volume = None
        
        # Optimización de respuesta de entrada
        pyautogui.PAUSE = 0
        pydirectinput.PAUSE = 0
        # -----------------------------------------------------------------
        # NUEVO: Inicialización del control de volumen de Windows
        # -----------------------------------------------------------------
        try:
            
            # Inicializamos COM para evitar fallos de inicialización en subprocesos o hilos
            comtypes.CoInitialize() 
            
            # Obtenemos el objeto de la clase AudioDevice
            speakers_device = AudioUtilities.GetSpeakers()
            
            if speakers_device:
                # La propiedad interna se encarga de llamar a .Activate() de forma nativa por ti
                self.volume = speakers_device.EndpointVolume
            else:
                self.volume = None
                print("[PRECAUCIÓN] No se detectaron altavoces activos.")
        except Exception as e:
            print(f"[PRECAUCIÓN] No se pudo inicializar el control de volumen por COM: {e}")
            self.volume = None
        # -----------------------------------------------------------------
        

    
    @staticmethod
    def ejecutar_en_hilo(func, *args, **kwargs):
        hilo = threading.Thread(target=func, args=args, kwargs=kwargs)
        hilo.daemon = True
        hilo.start()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def cargar(self): 
        try:
            path_json = self.resource_path("Comando.json")
            with open(path_json, 'r', encoding='utf-8') as archivo:
                self.datos = json.load(archivo)
            
            self.manoIzquierda = Mano(
                self.atajosManos[self.datos['Izquierda']['indice']],
                self.atajosManos[self.datos['Izquierda']['corazon']],
                self.atajosManos[self.datos['Izquierda']['anular']],
                self.atajosManos[self.datos['Izquierda']['menique']],
                None
            )
            self.manoDerecha = Mano(
                self.atajosManos[self.datos['Derecha']['indice']],
                self.atajosManos[self.datos['Derecha']['corazon']],
                self.atajosManos[self.datos['Derecha']['anular']],
                self.atajosManos[self.datos['Derecha']['menique']],
                None
            )
            
            if self.datos['Games']['estado'] == True:
                self.ModoGame()

        except FileNotFoundError:
            print(f"Error: El archivo Comando.json no fue encontrado.")
        except json.JSONDecodeError:
            print(f"Error: El archivo Comando.json no es un JSON válido.")
        except Exception as e:
            print(f"Ocurrió un error inesperado en cargar: {e}")       

    def guardar_datos(self):
        try:
            path_json = self.resource_path("Comando.json")
            with open(path_json, "w") as arch:
                json.dump(self.datos, arch, indent=4)
        except Exception as err:
            print(err)

    def inicio(self):
        while True:
            self.busqueda, self.imagen = self.__camara.read()
            if not self.busqueda:
                continue
                
            self.imagen = cv2.flip(self.imagen, 1)
            imgRGB = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB)
            imgRGB = np.ascontiguousarray(imgRGB)
            self.h, self.w, _ = self.imagen.shape
            
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
            timestamp_ms = int(time.time() * 1000)
            self.result = self.__manos.detect_for_video(mp_image, timestamp_ms)

            if self.result.hand_landmarks:
                for hand_landmarks_raw, handedness_raw in zip(self.result.hand_landmarks, self.result.handedness):
                    
                    # Dibujo manual seguro
                    for connection in self.__HAND_CONNECTIONS:
                        x1 = int(hand_landmarks_raw[connection[0]].x * self.w)
                        y1 = int(hand_landmarks_raw[connection[0]].y * self.h)
                        x2 = int(hand_landmarks_raw[connection[1]].x * self.w)
                        y2 = int(hand_landmarks_raw[connection[1]].y * self.h)
                        cv2.line(self.imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    for lm in hand_landmarks_raw:
                        cv2.circle(self.imagen, (int(lm.x * self.w), int(lm.y * self.h)), 5, (0, 0, 255), -1)

                    hand_landmarks = LandmarkWrapper(hand_landmarks_raw)
                    
                    # CORREGIDO: Asignar obligatoriamente a self.CVMano para que los métodos internos no den NoneType Error
                    self.CVMano = hand_landmarks 
                    
                    label = handedness_raw[0].category_name
                    handedness = HandednessWrapper(label)

                    if handedness and handedness.classification:
                        label = handedness.classification[0].label
                        if label == 'Right':
                            puntaindice = hand_landmarks.landmark[8]
                            puntapulgar = hand_landmarks.landmark[4]
                            self.__dedosCerrados(hand_landmarks)
                            
                            distanciaDed = self.__distanciaDedo(hand_landmarks)
                            
                            if self.__dedos_cerrados_estado == [False, True, True, True, False]:
                                x2, y2 = int(puntaindice.x * self.w), int(puntaindice.y * self.h)
                                x1, y1 = int(puntapulgar.x * self.w), int(puntapulgar.y * self.h)
                                p2, p1 = np.array([x2, y2]), np.array([x1, y1])
                                self.__volumen(p1, p2)
                            
                            if distanciaDed[0] < 25 and distanciaDed[1] < 25:
                                self.abrir_enlace_una_vez()
                            elif distanciaDed[0] < 25 and all(d > 25 for d in distanciaDed[1:]) and self.__dedos_cerrados_estado == [False, False, False, False, False]:
                                self.__press_alt_tab()
                        
                        elif label == 'Left':
                            distanciaDed = self.__distanciaDedo(hand_landmarks)
                            if distanciaDed[0] < 25:
                                x, y = hand_landmarks.landmark[8].x * self.w, hand_landmarks.landmark[8].y * self.h
                                if self.tX == 0 and self.tY == 0:
                                    self.tX, self.tY = x, y
                                # CORREGIDO: Pasamos los parámetros adaptados a la nueva firma de movermouseV2
                                self.__movermouseV2(x, y) 
                            else:
                                self.tX, self.tY = 0, 0    
                            
                            if distanciaDed[1] < 25 and distanciaDed[2] > 25:
                                pyautogui.click()
                            
                            if distanciaDed[2] < 25 and distanciaDed[1] > 25:
                                pyautogui.rightClick()
            
            cv2.imshow("Image", self.imagen)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.__camara.release()
        cv2.destroyAllWindows()

    def inicio2(self):
        self.busqueda, self.imagen = self.__camara.read()
        if not self.busqueda:
            return ""
            
        self.imagen = cv2.resize(self.imagen, (640, 480))
        self.imagen = cv2.flip(self.imagen, 1)
        imgRGB = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB)
        self.h, self.w, _ = self.imagen.shape
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        timestamp_ms = int(time.time() * 1000)
        self.result = self.__manos.detect_for_video(mp_image, timestamp_ms)

        if self.result.hand_landmarks:
            for hand_landmarks_raw, handedness_raw in zip(self.result.hand_landmarks, self.result.handedness):
                
                # Dibujo manual seguro
                for connection in self.__HAND_CONNECTIONS:
                    x1 = int(hand_landmarks_raw[connection[0]].x * self.w)
                    y1 = int(hand_landmarks_raw[connection[0]].y * self.h)
                    x2 = int(hand_landmarks_raw[connection[1]].x * self.w)
                    y2 = int(hand_landmarks_raw[connection[1]].y * self.h)
                    cv2.line(self.imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                for lm in hand_landmarks_raw:
                    cv2.circle(self.imagen, (int(lm.x * self.w), int(lm.y * self.h)), 5, (0, 0, 255), -1)

                hand_landmarks = LandmarkWrapper(hand_landmarks_raw)
                self.CVMano = hand_landmarks
                label = handedness_raw[0].category_name
                handedness = HandednessWrapper(label)
                
                if handedness and handedness.classification:
                    label = handedness.classification[0].label
                    
                    if label == 'Right':
                        self.__dedosCerrados(hand_landmarks)
                        distanciaDed = self.__distanciaDedo(hand_landmarks)
                        
                        if self.__dedos_cerrados_estado == [False, True, True, True, False]:
                            self.__volumen()
                        elif self.__dedos_cerrados_estado == [False, False, False, False, False]:
                            if distanciaDed[0] < 25 and distanciaDed[1] < 25 and all(d > 25 for d in distanciaDed[2:]):
                                self.abrir_enlace_una_vez()
                            elif distanciaDed[0] < 25 and all(d > 25 for d in distanciaDed[1:]):
                                self.manoIzquierda.Indice()
                            elif distanciaDed[1] < 25 and all(d > 25 for d in distanciaDed[2:]):
                                self.manoIzquierda.Corazon()
                            elif distanciaDed[2] < 25 and all(d > 25 for d in distanciaDed[3:]):
                                self.manoIzquierda.Anular()
                            elif distanciaDed[3] < 25 and all(d > 25 for d in distanciaDed[4:]):
                                # CORREGIDO: de mañique() a meñique() según la clase Mano típica
                                self.manoIzquierda.mañique() 
                            
                    elif label == 'Left':
                        distanciaDed = self.__distanciaDedo(hand_landmarks)
                        if distanciaDed[0] < 25:
                            self.manoDerecha.Indice()
                        elif distanciaDed[1] < 25 and distanciaDed[2] > 25:
                            self.manoDerecha.Corazon()
                        elif distanciaDed[2] < 25 and all(d > 25 for d in distanciaDed[3:]):
                            self.manoDerecha.Anular()
                        elif distanciaDed[3] < 25 and all(d > 25 for d in distanciaDed[4:]):
                            # CORREGIDO: de mañique() a meñique()
                            self.manoDerecha.mañique() 
                        else:
                            self.tX, self.tY = 0, 0 
                           
        _, buffer = cv2.imencode('.jpg', self.imagen)
        imagen_base64 = base64.b64encode(buffer).decode('utf-8')
        return imagen_base64

    def precionarTecla(self, d=0.5, t='w'):
        def tarea():
            pydirectinput.keyDown(t)
            time.sleep(d)
            pydirectinput.keyUp(t)
        threading.Thread(target=tarea, daemon=True).start()    
         
    def __dedosCerrados(self, hand_landmarks):
        self.__dedos_cerrados_estado = []
        landmarks_coords = []
        for lm in hand_landmarks.landmark:
            landmarks_coords.append(np.array([lm.x * self.w, lm.y * self.h, lm.z * self.w]))
            
        puntos_dedos_largos = {
            "indice": {"punta": 8, "base": 6},
            "corazon": {"punta": 12, "base": 10},
            "anular": {"punta": 16, "base": 14},
            "menique": {"punta": 20, "base": 18}
        }
        
        UMBRAL_Y_CERRADO_DEDOS = 20  
        UMBRAL_Z_CERRADO_DEDOS = 15  
        UMBRAL_DISTANCIA_REL_DEDOS = 0.7 
        puntos_palma_indices = [0, 1, 5, 9, 13, 17]
        coordenadas_palma = [landmarks_coords[i] for i in puntos_palma_indices]
        centro_palma = np.mean(np.array(coordenadas_palma), axis=0)
        
        for dedo_nombre, indices in puntos_dedos_largos.items():
            punta_coords = landmarks_coords[indices["punta"]]
            base_coords = landmarks_coords[indices["base"]]
            y_tip_below_y_base = punta_coords[1] > base_coords[1] + UMBRAL_Y_CERRADO_DEDOS
            z_tip_behind_z_base = punta_coords[2] > base_coords[2] + UMBRAL_Z_CERRADO_DEDOS
            distancia_punta_a_centro = np.linalg.norm(punta_coords - centro_palma)
            distancia_base_a_centro = np.linalg.norm(base_coords - centro_palma)
            distancia_relativa_es_menor = distancia_punta_a_centro < distancia_base_a_centro * UMBRAL_DISTANCIA_REL_DEDOS
            es_cerrado = (y_tip_below_y_base and z_tip_behind_z_base) or distancia_relativa_es_menor
            self.__dedos_cerrados_estado.append(es_cerrado)
            
        punta_pulgar_coords = landmarks_coords[4]
        base_pulgar_coords = landmarks_coords[2]
        UMBRAL_X_CERRADO_PULGAR = 35 
        UMBRAL_Z_CERRADO_PULGAR = 10 
        
        dist_x_punta_base_pulgar = abs(punta_pulgar_coords[0] - base_pulgar_coords[0])
        dist_x_punta_indice_base = abs(punta_pulgar_coords[0] - landmarks_coords[5][0])
        
        es_pulgar_lateralmente_cerrado = dist_x_punta_base_pulgar < UMBRAL_X_CERRADO_PULGAR or dist_x_punta_indice_base < UMBRAL_X_CERRADO_PULGAR * 1.5
        es_pulgar_profundidad_cerrado = punta_pulgar_coords[2] > base_pulgar_coords[2] + UMBRAL_Z_CERRADO_PULGAR
        es_pulgar_y_cerrado = punta_pulgar_coords[1] > base_pulgar_coords[1] + UMBRAL_Y_CERRADO_DEDOS / 2 
        
        es_pulgar_cerrado = (es_pulgar_lateralmente_cerrado or es_pulgar_y_cerrado) and es_pulgar_profundidad_cerrado
        self.__dedos_cerrados_estado.append(es_pulgar_cerrado)
 
    def __distanciaDedo(self, hand_landmarks):
        pulgar_x = hand_landmarks.landmark[4].x * self.w
        pulgar_y = hand_landmarks.landmark[4].y * self.h
        distancia = []
        for i in [8, 12, 16, 20]:
            pt = hand_landmarks.landmark[i]
            distancia.append(math.hypot(pt.x * self.w - pulgar_x, pt.y * self.h - pulgar_y))
        return distancia
  
    def __volumen(self, p1=None, p2=None):
        if p1 is not None and p2 is not None:
            distancia_pixeles = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        else:
            if self.CVMano is None: 
                return
            puntaindice = self.CVMano.landmark[8]
            puntapulgar = self.CVMano.landmark[4]
            x2, y2 = puntaindice.x * self.w, puntaindice.y * self.h
            x1, y1 = puntapulgar.x * self.w, puntapulgar.y * self.h
            distancia_pixeles = math.hypot(x2 - x1, y2 - y1)
        
        # Mapeo inteligente usando escalares (0.0 a 1.0 / 0% a 100%)
        # 20px (dedos juntos) -> 0% volumen | 160px (dedos separados) -> 100% volumen
        porcentaje = np.interp(distancia_pixeles, [20, 160], [0, 100])
        porcentaje = max(0, min(100, porcentaje)) # Asegura que se mantenga entre 0 y 100
        
        try:
            # SetMasterVolumeLevelScalar acepta valores de 0.0 a 1.0 de forma lineal
            self.volume.SetMasterVolumeLevelScalar(porcentaje / 100, None)
        except Exception as e:
            print(f"Error al cambiar volumen: {e}") 
    def __press_alt_tab(self, duration=0.5, n=1):
        try:
            pyautogui.keyDown('alt')
            for i in range(n):
                pyautogui.press('tab')
                time.sleep(duration)
            pyautogui.keyUp('alt')    
        except Exception as e:
            print(f"{e}")
  
    def abrir_enlace_una_vez(self):
        if not self.__enlace_principal_abierto:
            webbrowser.open_new_tab(self.__URL_PRINCIPAL)
            print(f"Abriendo el navegador con el enlace: {self.__URL_PRINCIPAL}")
            self.__enlace_principal_abierto = True
   
    def __moverMouseSuavizado(self):
        def tarea():
            try:
                if self.CVMano is None: return
                self.x = self.CVMano.landmark[8].x * self.w
                self.y = self.CVMano.landmark[8].y * self.h
                
                if ((self.x > (self.w / 2) - 20 and self.x < self.w - 20) and (self.y < self.h - 30 and self.y > 30)):
                    x3 = np.interp(self.x, [(self.w / 2) - 20, self.w - 20], [0, self.__anchopanta])
                    y3 = np.interp(self.y, [30, self.h - 30], [0, self.__altopanta])    

                    cubix = self.pubix + (x3 - self.pubix) / self.__ventana_suavizado
                    cubiy = self.pubiy + (y3 - self.pubiy) / self.__ventana_suavizado

                    pyautogui.moveTo(cubix, cubiy)
                    self.pubix, self.pubiy = cubix, cubiy
            except Exception as e:
                print(f"error {e}")
        threading.Thread(target=tarea, daemon=True).start()  
        
    def Scroll(self):
        try:
            if self.CVMano is None: return
            y = self.CVMano.landmark[20].y * self.h
            if y < self.h / 2:
                print('arriba')
                pyautogui.scroll(100)
            else:
                print('abajo')
                pyautogui.scroll(-100)
            time.sleep(0.5)
        except Exception as e:
            print(e)
        
    def setSuavisado(self, c):
        self.__ventana_suavizado = c
  
    # CORREGIDO: Firma modificada para aceptar parámetros opcionales y evitar fallos en 'inicio()'
    def __movermouseV2(self, x=None, y=None):
        try:
            if x is not None and y is not None:
                self.x, self.y = x, y
            else:
                if self.CVMano is None: return
                self.x = self.CVMano.landmark[8].x * self.w
                self.y = self.CVMano.landmark[8].y * self.h

            if self.tX == 0 and self.tY == 0:
                self.tX, self.tY = self.x, self.y
                return

            dx = self.x - self.tX
            dy = self.y - self.tY

            dist = math.sqrt(dx**2 + dy**2)
            if dist == 0:
                return

            nx = dx / dist
            ny = dy / dist

            if dist > 1:
                dist = 1

            velocidad = dist * 20
            pyautogui.moveRel(nx * velocidad, ny * velocidad)

        except Exception as e:
            print(f"Error en __movermouseV2: {e}")

    def setUrl(self, url):
        self.__URL_PRINCIPAL = url
    
    def set_datos(self, direccion, datos):
        self.datos[direccion] = datos

    def setManoIz(self, indices):
        self.manoIzquierda.setIndice(self.atajosManos[indices[0]])
        self.manoIzquierda.setCorazon(self.atajosManos[indices[1]])
        self.manoIzquierda.setAnular(self.atajosManos[indices[2]])
        # CORREGIDO: setMeñique con consistencia ortográfica
        self.manoIzquierda.setMeñique(self.atajosManos[indices[3]]) 
        
    def setManoDe(self, indices):
        self.manoDerecha.setIndice(self.atajosManos[indices[0]])
        self.manoDerecha.setCorazon(self.atajosManos[indices[1]])
        self.manoDerecha.setAnular(self.atajosManos[indices[2]])
        # CORREGIDO: setMeñique con consistencia ortográfica
        self.manoDerecha.setMeñique(self.atajosManos[indices[3]])

    def ModoGame(self):
        self.manoIzquierda.setIndice(self.modoGames['indice'])
        self.manoIzquierda.setCorazon(self.modoGames['corazon'])
        self.manoIzquierda.setAnular(self.modoGames['anular'])
        # CORREGIDO: Llamada al diccionario corregido 'menique'
        self.manoIzquierda.setMeñique(self.modoGames['menique']) 
        self.manoDerecha.setAnular(self.modoGames['mouse'])