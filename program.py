import time
import RPi.GPIO as GPIO
from lib import Database, MoistureSensor, TemperatureSensor

# Setup GPIO stuff
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

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

    previous_status_led1 = False
    previous_status_led2 = False
    previous_status_led3 = False
    previous_status_led4 = False
    previous_status_pomp = False

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

        # Control LED1 (dark red)
        led1 = database.selectOutput("LED1")
        if (int(led1[2]) == 1):
            GPIO.output(24, 0)
        else:
            GPIO.output(24, 1)
        # GPIO.output(24, int(led1[2]))
        if previous_status_led1 != bool(int(led1[2])):
            previous_status_led1 = bool(int(led1[2]))
            database.insertStatus(previous_status_led1, "LED1")

        # Control LED2 (red)
        led2 = database.selectOutput("LED2")
        if (int(led2[2]) == 1):
            GPIO.output(27, 0)
        else:
            GPIO.output(27, 1)
        # GPIO.output(27, int(led2[2]))
        if previous_status_led2 != bool(int(led2[2])):
            previous_status_led2 = bool(int(led2[2]))
            database.insertStatus(previous_status_led2, "LED2")
        
        # Control LED3 (blue)
        led3 = database.selectOutput("LED3")
        if (int(led3[2]) == 1):
            GPIO.output(22, 0)
        else:
            GPIO.output(22, 1)
        # GPIO.output(22, int(led3[2]))
        if previous_status_led3 != bool(int(led3[2])):
            previous_status_led3 = bool(int(led3[2]))
            database.insertStatus(previous_status_led3, "LED3")
        # Control LED4 (white)
        led4 = database.selectOutput("LED4")
        GPIO.output(17, int(led4[2]))
        if previous_status_led4 != bool(int(led4[2])):
            previous_status_led4 = bool(int(led4[2]))
            database.insertStatus(previous_status_led4, "LED4")

        # Control POMP
        pomp = database.selectOutput("POMP")
        GPIO.output(23, int(pomp[2]))
        if previous_status_pomp != bool(int(pomp[2])):
            previous_status_pomp = bool(int(pomp[2]))
            database.insertStatus(previous_status_pomp, "POMP")

        time.sleep(1)

if __name__ == '__main__':
    main()
