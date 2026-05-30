from fastapi import FastAPI
from pydantic import BaseModel
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
history = []

class InventoryData(BaseModel):
    data: dict

class EventData(BaseModel):
    event: str

# =========================
# INVENTARIO
# =========================
@app.post("/inventory")
def update_inventory(payload: InventoryData):
    global inventory
    # El inventario ya viene estabilizado desde Deteccion_1_2.py
    # No se generan eventos aquí para evitar duplicados
    inventory = payload.data
    return {"status": "ok"}

@app.get("/inventory")
def get_inventory():
    return inventory

# =========================
# HISTORIAL
# =========================
@app.post("/history")
def add_event(payload: EventData):
    global history
    history.append(payload.event)
    # Mantener solo los últimos 200 eventos
    if len(history) > 200:
        history = history[-200:]
    return {"status": "ok"}

@app.get("/history")
def get_history():
    return history[-50:]