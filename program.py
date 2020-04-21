import time
import RPi.GPIO as GPIO
from lib import Database, MoistureSensor, TemperatureSensor

# Setup GPIO stuff
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

# Create instances of components
database = Database("provil-ict.be", "gip_agritower", "agritower", "gip_2019_agritower")
moisture_sensor = MoistureSensor(0)
temperature_sensor = TemperatureSensor()

# Main program
def main():
    count = 0

    print "Program has started"

    while True:
        count += 1

        # Loop every second -> 10 = 10 seconds
        if count == 10:
            count = 0
            print "Getting sensor data"
            database.insertMoisture(moisture_sensor.getMoisture())
            database.insertTemperature(temperature_sensor.getTemperature())

        # Control LED1
        led1 = database.selectOutput("LED1")
        GPIO.output(23, int(led1[2]))
        
        time.sleep(1)

if __name__ == '__main__':
    main()
