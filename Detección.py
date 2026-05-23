from ultralytics import YOLO
import cv2

# Cargar modelo YOLO
model = YOLO("yolov8n.pt")

# URL de IP Webcam
url = "http://100.118.162.221:8080/video"

# Abrir stream
cap = cv2.VideoCapture(url)

# Crear ventana redimensionable
cv2.namedWindow("YOLO IP Webcam", cv2.WINDOW_NORMAL)

# Tamaño de ventana
cv2.resizeWindow("YOLO IP Webcam", 600, 400)

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir video")
        break

    # Detectar objetos
    results = model(frame)

    # Dibujar cajas
    annotated_frame = results[0].plot()

    # Mostrar ventana
    cv2.imshow("YOLO IP Webcam", annotated_frame)

    # ESC para salir
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()