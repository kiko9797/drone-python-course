from sqlalchemy import Column, Integer,String
from database import Base

class DroneDB(Base):
    __tablename__ =  "drones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    battery = Column(Integer, default=100)
    drone_type = Column(String)