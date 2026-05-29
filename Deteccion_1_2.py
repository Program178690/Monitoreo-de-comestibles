from ultralytics import YOLO
import cv2
from datetime import datetime
import requests

# =========================
# CARGAR MODELO
# =========================
model = YOLO("yolov8n.pt")

# =========================
# URL IP WEBCAM
# =========================
url = "http://100.81.71.252:8080/video"
cap = cv2.VideoCapture(url)

# =========================
# VENTANA
# =========================
cv2.namedWindow("YOLO Inventario", cv2.WINDOW_NORMAL)
cv2.resizeWindow("YOLO Inventario", 680, 420)

# =========================
# ESTADO GENERAL
# =========================
last_detected = {}

# 🔥 NUEVO: memoria inteligente
object_memory = {}
missing_threshold = 5  # frames para considerar desaparecido

frame_count = 0
frame_id = 0

# =========================
# LOOP PRINCIPAL
# =========================
while True:

    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir video")
        break

    frame_count += 1
    frame_id += 1

    # =========================
    # ANALIZAR 1 FRAME SÍ, 1 NO
    # =========================
    if frame_count % 2 != 0:
        continue

    # =========================
    # DETECCIÓN YOLO
    # =========================
    results = model(frame, imgsz=320, conf=0.5)
    names = results[0].names

    current_detected = {}

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        object_name = names[class_id]

        current_detected[object_name] = current_detected.get(object_name, 0) + 1

    # =========================
    # 🔥 DETECCIÓN DE EVENTOS INTELIGENTES
    # =========================
    events = []

    # actualizar memoria de objetos vistos
    for obj in current_detected:
        object_memory[obj] = frame_id

        # detectar aparición (solo si es nuevo)
        if obj not in last_detected:
            events.append(f"apareció {obj}")

    # detectar desapariciones
    for obj in list(object_memory.keys()):
        last_seen = object_memory[obj]

        if frame_id - last_seen > missing_threshold:
            events.append(f"desapareció {obj}")
            del object_memory[obj]

    # =========================
    # ENVIAR A FASTAPI (solo inventario actual)
    # =========================
    try:
        requests.post(
            "http://127.0.0.1:8000/inventory",
            json={"data": current_detected}
        )
    except Exception as e:
        print("Error enviando a FastAPI:", e)

    # =========================
    # HISTORIAL (SOLO EVENTOS INTELIGENTES)
    # =========================
    if events:

        now = datetime.now().strftime("%H:%M:%S")

        try:
            with open("historial.txt", "r") as history:
                lines = history.readlines()
        except FileNotFoundError:
            lines = []

        new_entry = [f"\n[{now}] EVENTOS\n"]

        for e in events:
            new_entry.append(e + "\n")

        events_history = "".join(lines).split("\n[")
        events_history = [e for e in events_history if e.strip()]
        events_history.append("".join(new_entry))
        events_history = events_history[-50:]

        with open("historial.txt", "w") as history:
            for i, event in enumerate(events_history):
                if i != 0 and not event.startswith("["):
                    history.write("\n[" + event)
                else:
                    history.write(event)

        # terminal
        print("\nEVENTOS:")
        for e in events:
            print("-", e)

    # =========================
    # GUARDAR ESTADO
    # =========================
    last_detected = current_detected.copy()

    # =========================
    # VIDEO
    # =========================
    annotated = results[0].plot()
    cv2.imshow("YOLO Inventario", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()