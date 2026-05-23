from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

# ⭐ NUEVO: CORS para conectar con HTML/JS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción luego se restringe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

inventory = {}
history = []  # 🔥 aquí guardamos eventos

class InventoryData(BaseModel):
    data: dict

@app.post("/inventory")
def update_inventory(payload: InventoryData):

    global inventory, history

    new_data = payload.data
    now = datetime.now().strftime("%H:%M:%S")

    # =========================
    # DETECTAR CAMBIOS
    # =========================
    appeared = []
    disappeared = []

    for obj, count in new_data.items():
        if obj not in inventory:
            appeared.append(obj)
        elif inventory[obj] != count:
            appeared.append(obj)

    for obj in inventory:
        if obj not in new_data:
            disappeared.append(obj)

    # =========================
    # EVENTOS
    # =========================
    for obj in appeared:
        history.append(f"[{now}] apareció {obj}")

    for obj in disappeared:
        history.append(f"[{now}] desapareció {obj}")

    inventory = new_data

    return {"status": "ok"}

@app.get("/inventory")
def get_inventory():
    return inventory

@app.get("/history")
def get_history():
    return history[-50:]