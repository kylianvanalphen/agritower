from grove_moisture_sensor import GroveMoistureSensor

class MoistureSensor():
    def __init__(self, pin):
        self.sensor = GroveMoistureSensor(pin)

    def getMoisture(self):
        return self.sensor.moisture()

    def getMoistureText(self):
        moisture = self.getMoisture()

        if 0 <= moisture and moisture < 300:
            result = 'Dry'
        elif 300 <= moisture and moisture < 600:
            result = 'Moist'
        else:
            result = 'Wet'
        
        return result