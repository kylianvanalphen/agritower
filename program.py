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

    database.moveMoistureArchive()
    database.moveTemperatureArchive()
    print "Moved data to archive"
    previous_status_led = False
    while True:
        count += 1

        # Loop every second -> 10 = 10 seconds
        if count % 10 == 0:
            print "Getting sensor data"
            database.insertMoisture(moisture_sensor.getMoisture())
            database.insertTemperature(temperature_sensor.getTemperature())

        # Move to archive every hour
        if count == 3600:
            count = 0
            database.moveMoistureArchive()
            database.moveTemperatureArchive()
            print "Moved data to archive"

        # Control LED1
        led1 = database.selectOutput("LED1")
        GPIO.output(23, int(led1[2]))
        if previous_status_led != bool(int(led1[2])):
            previous_status_led = bool(int(led1[2]))
            database.insertStatus(previous_status_led, "LED1")

        # Control LED2
        # led2 = database.selectOutput("LED2")
        # GPIO.output(24, int(led2[2]))
        
        time.sleep(1)

if __name__ == '__main__':
    main()
