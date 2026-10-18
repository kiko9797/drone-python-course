from fastapi import FastAPI, HTTPException  
from drone_course import Drone, CargoDrone, RacingDrone
from pydantic import BaseModel, Field

app = FastAPI()

class FlyRequest(BaseModel):
    minutes: int = Field(ge=0)

class ChargeRequest(BaseModel):
    charge: int = Field(ge=0, le=100)

fleet = {
    "Alpha": Drone("Alpha", 100),
    "Heavy": CargoDrone("Heavy", 100),
    "Speedy": RacingDrone("Speedy", 100, 250)
}

@app.get("/status/{name_drone}")
def get_status(name_drone: str):
    if name_drone not in fleet:
        raise HTTPException(status_code=404, detail="Дрон не найден")
    
    dron = fleet[name_drone] # Достаем дрона ПОСЛЕ проверки
    return {"имя": dron.name, "заряд": dron.battery}

@app.post("/fly/{name_drone}")
def fly_drone(name_drone: str, request: FlyRequest):
    if name_drone not in fleet:
        raise HTTPException(status_code=404, detail="Дрон не найден")
    
    dron = fleet[name_drone]
    dron.fly(request.minutes) # Заставляем лететь ОБЪЕКТ
    return {"status": "success", "battery_left": dron.battery}

@app.post("/charge/{name_drone}")
def charge_drone(name_drone: str, request: ChargeRequest):
    if name_drone not in fleet:
        raise HTTPException(status_code=404, detail="Дрон не найден")
    
    dron = fleet[name_drone]
    dron.charge(request.charge)
    return {"status": "charged", "battery_now": dron.battery}