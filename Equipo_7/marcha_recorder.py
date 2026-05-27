import cv2
import mediapipe as mp
import serial
import time
import csv
import numpy as np

# Configuración de MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Conexión Serial
try:
    ser = serial.Serial('COM4', 115200)
    print("Conexión con ESP32 exitosa")
except:
    print("No se encontró el ESP32 en COM4")
    ser = None

# Configuración de captura
cap = cv2.VideoCapture(0)
kinematics_data = []

print("Cámara lista. Presiona ESC para salir.")

while True:
    success, frame = cap.read()
    if not success:
        break

    # Procesar Pose
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    # Dibujar Landmarks y calcular ángulo
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Obtener puntos de referencia
        landmarks = results.pose_landmarks.landmark
        hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y])
        knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y])
        ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])
        
        # Calcular ángulo
        radians = np.arctan2(ankle[1]-knee[1], ankle[0]-knee[0]) - np.arctan2(hip[1]-knee[1], hip[0]-knee[0])
        angle = np.abs(np.degrees(radians))
        if angle > 180.0:
            angle = 360 - angle
            
        # Mostrar texto en pantalla
        cv2.putText(frame, f'Angulo Rodilla: {int(angle)}', (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Leer EMG
    if ser is not None and ser.in_waiting > 0:
        linea_emg = ser.readline().decode('utf-8').rstrip()
        print(f"EMG: {linea_emg}")

    cv2.imshow('Analisis de Marcha', frame)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
if ser:
    ser.close()