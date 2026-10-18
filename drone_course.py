class Drone:
    def __init__ (self, name,battery):
        self.name = name
        self.battery = battery
    def fly(self,minutes):
        self.battery = self.battery - minutes * 2 
        if self.battery<0:
            self.battery = 0
    def __str__(self):
        
        return f"{self.name}: {self.battery}% "

    def charge(self,amount):  
        if amount < 0: 
            raise ValueError("Charge amount cannot be negative")
        self.battery += amount 
        if self.battery> 100:
            self.battery = 100


class CargoDrone(Drone):
    def fly(self,minutes):
        self.battery = self.battery - minutes * 3
        if self.battery < 0:
            self.battery = 0



class RacingDrone(Drone):
    def __init__(self,name,battery,max_speed):
        super().__init__(name,battery)
        self.max_speed = max_speed

    def fly(self,minutes):
        self.battery = self.battery - minutes * 4
        if self.battery < 0:
            self.battery = 0

    def __str__(self):
        base_text = super().__str__()
        return f"{base_text}, {self.max_speed} км/ч"




    







