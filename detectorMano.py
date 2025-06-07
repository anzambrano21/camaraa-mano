import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import autopy
from mano import Mano
import base64


class CVMano:



    def __init__(self):
        self.__URL_PRINCIPAL = 'https://www.youtube.com/watch?v=44pt8w67S8I'
        self.__camara = cv2.VideoCapture(0)
        self.__Mpmanos = mp.solutions.hands
        self.__manos = self.__Mpmanos.Hands(static_image_mode=False,
                                            max_num_hands=2,
                                            min_detection_confidence=0.9,
                                            min_tracking_confidence=0.8)
        self.__mpDibujar = mp.solutions.drawing_utils
        self.__enlace_principal_abierto = False
        self.__dedos_cerrados_estado = []
        self.__ventana_suavizado = 5
        self.pubix, self.pubiy = 0, 0
        self.__anchopanta, self.__altopanta = autopy.screen.size()
        self.tX=0
        self.tY =0
        self.x,self.y=0,0
        self.manoDerecha=Mano(self.__moverMouseSuavizado,pyautogui.click,pyautogui.rightClick,self.Scroll)
        self.manoIzquierda=Mano(self.__press_alt_tab,self.__press_alt_tab2,self.__press_alt_tab3,self.__press_alt_tab4)
        self.CVMano=None
        
    def inicio(self):
        while True:
            
            # Verificar si la cámara está abierta
            self.busqueda, self.imagen = self.__camara.read()
            self.imagen = cv2.flip(self.imagen, 1)
            imgRGB = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB)
            self.h, self.w, _ = self.imagen.shape
            self.result = self.__manos.process(imgRGB)

            if self.result.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(self.result.multi_hand_landmarks, self.result.multi_handedness):
                    self.__mpDibujar.draw_landmarks(self.imagen, hand_landmarks, self.__Mpmanos.HAND_CONNECTIONS)
                    if handedness and handedness.classification:
                        label = handedness.classification[0].label
                        if label == 'Left':
                            puntaindice = hand_landmarks.landmark[8]  # Nodo 8
                            puntapulgar = hand_landmarks.landmark[4]
                            self.__dedosCerrados(hand_landmarks)
                            print(self.__dedos_cerrados_estado)
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
                        
                        elif label == 'Right':
                            
                            distanciaDed = self.__distanciaDedo(hand_landmarks)
                            if distanciaDed[0] < 25:
                                x, y = hand_landmarks.landmark[8].x *  self.w, hand_landmarks.landmark[8].y  * self.h
                                if(self.tY==0 and self.tX==0):
                                    self.tX,self.tY=x,y
                                self.__movermouseV2(x,y)
                                #self.__moverMouseSuavizado(x, y)
                            else:
                                self.tX,self.tY=0,0    
                            if distanciaDed[1] < 25 and distanciaDed[2] > 25:
                                pyautogui.click()
                            
                            if distanciaDed[2] < 25 and distanciaDed[1] > 25:
                                pyautogui.rightClick()
            
            cv2.imshow("Image", self.imagen)

            # Salir con la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Liberar recursos al finalizar
        self.__camara.release()
        cv2.destroyAllWindows()
    def inicio2(self):
        
            
            # Verificar si la cámara está abierta
            self.busqueda, self.imagen = self.__camara.read()
            self.imagen = cv2.flip(self.imagen, 1)
            imgRGB = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB)
            self.h, self.w, _ = self.imagen.shape
            self.result = self.__manos.process(imgRGB)

            if self.result.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(self.result.multi_hand_landmarks, self.result.multi_handedness):
                    self.__mpDibujar.draw_landmarks(self.imagen, hand_landmarks, self.__Mpmanos.HAND_CONNECTIONS)
                    self.CVMano=hand_landmarks
                    if handedness and handedness.classification:
                        label = handedness.classification[0].label
                        
                        if label == 'Left':
                            
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
                                    self.manoIzquierda.Anular()  # Agregado si falta referencia a dedo anular
                                elif distanciaDed[3] < 25 and all(d > 25 for d in distanciaDed[4:]):
                                    self.manoIzquierda.mañique()
                                else:
                                    print("No se detectó ningún gesto válido.")  # Mensaje de depuración
                        
                        elif label == 'Right':
                            
                            distanciaDed = self.__distanciaDedo(hand_landmarks)
                            if distanciaDed[0] < 25:
                                
                                self.manoDerecha.Indice()
                               
                            if distanciaDed[1] < 25 and distanciaDed[2] > 25:
                                self.tX,self.tY=0,0 
                                self.manoDerecha.Corazon()
                            
                            elif distanciaDed[2] < 25 and distanciaDed[1] > 25:
                                self.manoDerecha.Anular()
                            
                                self.tX,self.tY=0,0 
            # --- ¡AQUÍ ESTÁ LA PARTE CRÍTICA QUE FALTA EN TU CÓDIGO ACTUAL! ---
            # Codificar la imagen (array NumPy de OpenCV) a formato JPEG en un búfer
            _, buffer = cv2.imencode('.jpg', self.imagen)
            # Convertir el búfer (bytes JPEG) a una cadena Base64
            imagen_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return imagen_base64 # Retorna la cadena Base64 que Flet necesita


        # Liberar recursos al finalizar


    def __dedosCerrados(self,hand_landmarks):
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
            interseccion_pulgar_coords = landmarks_coords[3] 
            UMBRAL_X_CERRADO_PULGAR = 35 
            UMBRAL_Z_CERRADO_PULGAR = 10 
            dist_x_punta_base_pulgar = abs(punta_pulgar_coords[0] - base_pulgar_coords[0])
            dist_x_punta_indice_base = abs(punta_pulgar_coords[0] - landmarks_coords[5][0])
            es_pulgar_lateralmente_cerrado = dist_x_punta_base_pulgar < UMBRAL_X_CERRADO_PULGAR or dist_x_punta_indice_base < UMBRAL_X_CERRADO_PULGAR * 1.5
            es_pulgar_profundidad_cerrado = punta_pulgar_coords[2] > base_pulgar_coords[2] + UMBRAL_Z_CERRADO_PULGAR
            es_pulgar_y_cerrado = punta_pulgar_coords[1] > base_pulgar_coords[1] + UMBRAL_Y_CERRADO_DEDOS / 2 
            es_pulgar_cerrado = (es_pulgar_lateralmente_cerrado or es_pulgar_y_cerrado) and es_pulgar_profundidad_cerrado
            self.__dedos_cerrados_estado.append(es_pulgar_cerrado)
    def __distanciaDedo(self,hand_landmarks):
        puntaded=[8,12,16,20]
        pulgar = np.array([hand_landmarks.landmark[4].x * self.w, hand_landmarks.landmark[4].y * self.h])
        puntos=[np.array([int(hand_landmarks.landmark[i].x*self.w),int(hand_landmarks.landmark[i].y*self.h)]) for i in puntaded]
        distancia=[np.linalg.norm(puntos[i]-pulgar) for i in range(len(puntos))]
        return distancia
    def __volumen(self):
        puntaindice = self.CVMano.landmark[8]  # Nodo 8
        puntapulgar = self.CVMano.landmark[4]
        x2, y2 = int(puntaindice.x * self.w), int(puntaindice.y * self.h)
        x1, y1 = int(puntapulgar.x * self.w), int(puntapulgar.y * self.h)
        p2, p1 = np.array([x2, y2]), np.array([x1, y1])
        porcentaje = np.linalg.norm(p2-p1)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        porcentaje = max(0, min(100, porcentaje))
        volume.SetMasterVolumeLevelScalar(porcentaje / 100, None)
    def __press_alt_tab(self,duration=0.5):
        try:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep(duration)
            pyautogui.keyUp('alt')
            
        except Exception as e:
            print(f"{e}")
    def __press_alt_tab2(self,duration=0.5):
        try:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.press('tab')
            time.sleep(duration)
            pyautogui.keyUp('alt')
            
        except Exception as e:
            print(f"{e}")
    def __press_alt_tab3(self,duration=0.5):
        try:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            time.sleep(duration)
            pyautogui.keyUp('alt')
            
        except Exception as e:
            print(f"{e}")
    def __press_alt_tab4(self,duration=0.5):
        try:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
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
        try:
            self.x=self.CVMano.landmark[8].x*self.w
            self.y=self.CVMano.landmark[8].y*self.h
            
            if((self.x>(self.w/2)-20 and self.x<self.w-20 ) and (self.y<self.h-30 and self.y>30)):
                x3 = np.interp(self.x, [(self.w/2)-20, self.w-20], [0, self.__anchopanta])  # Lista correcta

                y3 = np.interp(self.y, [30,self.h-30  ], [0, self.__altopanta])    

                cubix = self.pubix + (x3 - self.pubix) / self.__ventana_suavizado
                cubiy = self.pubiy + (y3 - self.pubiy) / self.__ventana_suavizado

                autopy.mouse.move(cubix,cubiy) 
                self.pubix, self.pubiy = cubix, cubiy
        except Exception as e:
            print(f"{e}")
    def __movermouseV2(self):
            self.x, self.y = self.hand_landmarks.landmark[8].x *  self.w, self.hand_landmarks.landmark[8].y  * self.h
            if(self.tY==0 and self.tX==0):
                self.tX,self.tY=self.x,self.y
            # Interpolar el movimiento para hacerlo más suave
            dx = self.x - self.tX
            dy = self.y - self.tY

            # Solo mover si la diferencia es significativa
            if abs(dx) > 5 or abs(dy) > 5:
                pyautogui.moveRel(dx * 0.3, dy * 0.3)  # Suavizado con factor 0.6

        # Actualizar la posición actual
        
    def Scroll(self):
        pyautogui.scroll(100)