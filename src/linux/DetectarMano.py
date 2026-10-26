import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import base64
# Conexiones estándar de los 21 puntos clave de la mano
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Pulgar
    (0, 5), (5, 6), (6, 7), (7, 8),        # Índice
    (5, 9), (9, 10), (10, 11), (11, 12),  # Medio
    (9, 13), (13, 14), (14, 15), (15, 16),# Anular
    (13, 17), (17, 18), (18, 19), (19, 20),# Meñique
    (0, 17)                                # Base de la palma
]
class CVMano:
    def __init__(self, camera_index=0):
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
        height, width, _ = frame.shape
        
        # OpenCV lee en BGR, MediaPipe Tasks requiere RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Realizar la detección
        detection_result = self.detector.detect(mp_image)

        # Dibujar los resultados si se detectan manos
        if detection_result.hand_landmarks:
            for hand_landmarks in detection_result.hand_landmarks:
                landmark_points = []
                
                # Obtener coordenadas en píxeles de cada punto clave
                for lm in hand_landmarks:
                    x = int(lm.x * width)
                    y = int(lm.y * height)
                    landmark_points.append((x, y))
                    # Dibujar el círculo rojo en cada articulación
                    cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)

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


if __name__ == '__main__':
    inicio = CVMano()
    while True:
        frame_b64 = inicio.get_Frame()
        if not frame_b64:
            break
        # Si se ejecuta directamente para pruebas
        if cv2.waitKey(5) & 0xFF == 27:
            break
    inicio.liberar()