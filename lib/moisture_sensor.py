from grove_moisture_sensor import GroveMoistureSensor

class MoistureSensor():
    def __init__(self, pin):
        self.sensor = GroveMoistureSensor(pin)

    def getMoisture(self):
        return self.sensor.moisture()