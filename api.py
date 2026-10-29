from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# Импортируем настройки базы и модель таблицы
from database import SessionLocal
from models import DroneDB

# Импортируем твои классы, чтобы использовать их логику (2%, 3%, 4%)
from drone_course import Drone, CargoDrone, RacingDrone

app = FastAPI()

# --- Модели запросов (Pydantic) ---
class FlyRequest(BaseModel):
    minutes: int = Field(ge=0)

class ChargeRequest(BaseModel):
    charge: int = Field(ge=0, le=100)

class CreateDroneRequest(BaseModel):
    name: str
    drone_type: str = "default" # default, cargo, racing

# --- Подключение к базе данных ---
# Эта функция открывает сессию для каждого запроса и закрывает её после
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Вспомогательная функция ---
# Она берет данные из базы и создает объект твоего класса
def get_drone_object(db_drone: DroneDB):
    if db_drone.drone_type == "cargo":
        return CargoDrone(db_drone.name, db_drone.battery)
    elif db_drone.drone_type == "racing":
        return RacingDrone(db_drone.name, db_drone.battery, 250) # 250 - макс скорость
    else:
        return Drone(db_drone.name, db_drone.battery)

# 1. СОЗДАНИЕ ДРОНА (Добавляем в базу)
@app.post("/drones")
def create_drone(request: CreateDroneRequest, db: Session = Depends(get_db)):
    # Проверяем, нет ли уже такого дрона
    existing = db.query(DroneDB).filter(DroneDB.name == request.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Дрон с таким именем уже есть")
    
    # Создаем нового
    new_drone = DroneDB(name=request.name, drone_type=request.drone_type, battery=100)
    db.add(new_drone)      # Кладем в корзину
    db.commit()            # Сохраняем в базу
    db.refresh(new_drone)  # Обновляем, чтобы получить ID
    
    return {"status": "success", "drone": new_drone.name, "type": new_drone.drone_type}

# 2. СТАТУС (Читаем из базы)
@app.get("/status/{name_drone}")
def get_status(name_drone: str, db: Session = Depends(get_db)):
    dron = db.query(DroneDB).filter(DroneDB.name == name_drone).first()
    if not dron:
        raise HTTPException(status_code=404, detail="Дрон не найден")
    
    return {"имя": dron.name, "заряд": dron.battery, "тип": dron.drone_type}

# 3. ПОЛЕТ (Меняем в базе)
@app.post("/fly/{name_drone}")
def fly_drone(name_drone: str, request: FlyRequest, db: Session = Depends(get_db)):
    dron_db = db.query(DroneDB).filter(DroneDB.name == name_drone).first()
    if not dron_db:
        raise HTTPException(status_code=404, detail="Дрон не найден")
    
    # Превращаем запись из базы в объект Python
    dron_obj = get_drone_object(dron_db)
    
    # Заставляем летать (используется логика 2%, 3% или 4%)
    dron_obj.fly(request.minutes)
    
    # Записываем новый заряд обратно в базу и сохраняем
    dron_db.battery = dron_obj.battery
    db.commit()
    
    return {"status": "success", "battery_left": dron_db.battery}

# 4. ЗАРЯДКА (Меняем в базе)
@app.post("/charge/{name_drone}")
def charge_drone(name_drone: str, request: ChargeRequest, db: Session = Depends(get_db)):
    dron_db = db.query(DroneDB).filter(DroneDB.name == name_drone).first()
    if not dron_db:
        raise HTTPException(status_code=404, detail="Дрон не найден")
    
    dron_obj = get_drone_object(dron_db)
    dron_obj.charge(request.charge)
    
    dron_db.battery = dron_obj.battery
    db.commit()
    
    return {"status": "charged", "battery_now": dron_db.battery}

@app.delete("/drones/{name_drone}")
def delete_drone(name_drone: str, db: Session = Depends(get_db)):
    drone_db = db.query(DroneDB).filter(DroneDB.name == name_drone).first()
    if not drone_db:
        raise HTTPException(status_code=404, detail="Дрон не найден")
    db.deleete(drone_db)
    db.commit()
    
    return {"status": "success", "message": f"Дрон {name_drone} удален"}