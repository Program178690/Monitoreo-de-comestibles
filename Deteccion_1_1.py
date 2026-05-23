from ultralytics import YOLO
import cv2

# Modelo YOLO
model = YOLO("yolov8n.pt")

# URL IP Webcam
url = "http://10.173.16.59:8080/video"

cap = cv2.VideoCapture(url)

# Ventana redimensionable
cv2.namedWindow("YOLO IP Webcam", cv2.WINDOW_NORMAL)
cv2.resizeWindow("YOLO IP Webcam", 680, 420)

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir video")
        break

    frame_count += 1

    # Saltar 1 de cada 2 frames
    if frame_count % 2 != 0:
        continue

    # YOLO más rápido y más estable
    results = model(
        frame,
        imgsz=320,
        conf=0.5
    )

    # Dibujar resultados
    annotated_frame = results[0].plot()

    cv2.imshow("YOLO IP Webcam", annotated_frame)

    # ESC para salir
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()