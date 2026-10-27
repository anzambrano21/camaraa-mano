from flet.controls.core import reorderable_drag_handle
from math import sqrt
import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import base64
from util.herramienta import HAND_CONNECTIONS
from src.linux.Acciones import Acciones
from src.linux.GestorGestos import GestorGestos
# Conexiones estándar de los 21 puntos clave de la mano

class CVMano:

    
    def __init__(self, camera_index=0):
        self.gestor = GestorGestos()
        self.ejecutor = Acciones()
        self._cooldowns = {}
        self._cooldown_ms = 500
        self.ultimo_landmarks = {}  # {"Left": [...], "Right": [...]}

        # Resolver ruta absoluta al modelo hand_landmarker.task
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        model_path = os.path.join(base_dir, 'hand_landmarker.task')
        
        # Configurar opciones de MediaPipe Tasks
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Crear el detector
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.cap = cv2.VideoCapture(camera_index)
        self.frame = ""

    def get_Frame(self):
        if not self.cap.isOpened():
            return self.frame

        success, frame = self.cap.read()
        if not success:
            return self.frame

        # Efecto espejo para mayor naturalidad
        frame = cv2.flip(frame, 1)
        self.height, self.width, _ = frame.shape
        
        # OpenCV lee en BGR, MediaPipe Tasks requiere RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Realizar la detección
        detection_result = self.detector.detect(mp_image)

        # Dibujar los resultados si se detectan manos
        if detection_result.hand_landmarks:
            for hand_landmarks, handedness in zip(detection_result.hand_landmarks, detection_result.handedness):
                landmark_points = []

                hand= handedness[0].category_name
                # Obtener coordenadas en píxeles de cada punto clave
                for lm in hand_landmarks:
                    x = int(lm.x * self.width)
                    y = int(lm.y * self.height)
                    landmark_points.append((x, y))
                    # Dibujar el círculo rojo en cada articulación
                    cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)

                
                # ANTES (borrar esto):
                distancia_pulgar_indice = self.Distancia(landmark_points[4], landmark_points[8])
                if hand == "Left":
                    if distancia_pulgar_indice < 30:
                        print("dedo indice y pulgar juntos")
                else:
                    print(distancia_pulgar_indice)

                # DESPUÉS (poner esto):
                self.ultimo_landmarks[hand] = landmark_points  # guardar para captura desde UI

                gesto = self.gestor.detectar_gesto(landmark_points, hand)
                if gesto and self._puede_ejecutar(gesto["nombre"]):
                    self.ejecutor.ejecutar(gesto["accion"])

                if hand == "Left":
                    if distancia_pulgar_indice < 30:
                        print("dedo indice y pulgar juntos")
                else:
                    print(distancia_pulgar_indice)

                # Dibujar las líneas verdes que conectan la estructura de la mano
                for connection in HAND_CONNECTIONS:
                    pt1_idx, pt2_idx = connection
                    pt1 = landmark_points[pt1_idx]
                    pt2 = landmark_points[pt2_idx]
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
                    
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        self.frame = base64.b64encode(buffer).decode('utf-8')
        return self.frame

    def liberar(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

    def Distancia(self,pt1,pt2):
        return sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)
    
    def dedos_extendidos(self,landmarks):
        """Retorna lista de 5 booleanos [pulgar, indice, corazon, anular, menique]"""
        dedos = []
        
        # Pulgar: comparar X del tip (4) vs X del IP (3)
        # Depende de la mano (izq/der), usar distancia al landmark 0
        dedos.append(self.Distancia(landmarks[4], landmarks[0]) > self.Distancia(landmarks[3], landmarks[0]))
        
        # Resto de dedos: tip.y < pip.y (en coordenadas de pantalla, Y crece hacia abajo)
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        for tip, pip in zip(tips, pips):
            dedos.append(landmarks[tip][1] < landmarks[pip][1])
        
        return dedos  

    def _puede_ejecutar(self, nombre_gesto):
        import time
        ahora = time.time() * 1000
        ultimo = self._cooldowns.get(nombre_gesto, 0)
        if ahora - ultimo > self._cooldown_ms:
            self._cooldowns[nombre_gesto] = ahora
            return True
        return False
    
    def obtener_landmarks(self, mano="Left"):
        """La UI llama esto cuando el usuario presiona 'Capturar Gesto'"""
        return self.ultimo_landmarks.get(mano, None)
    
