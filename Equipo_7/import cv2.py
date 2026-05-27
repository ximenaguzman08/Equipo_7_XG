import cv2
import mediapipe as mp
import serial
import time
import csv

# Intentar conectar con el ESP32 (si falla, el código te avisará)
try:
    ser = serial.Serial('COM4', 115200)
    print("Conexión con ESP32 exitosa")
except:
    print("No se encontró el ESP32 en COM4, revisa tu puerto")
    ser = None

cap = cv2.VideoCapture(0)
print("Si ves este mensaje, la cámara está lista.")

while True:
    success, frame = cap.read()
    if not success: break
    
    cv2.imshow('Ventana de Prueba', frame)
    if cv2.waitKey(1) == 27: # ESC
        break

cap.release()
cv2.destroyAllWindows()