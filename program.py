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

        print "Loop %i" % count

        # Loop every second -> 10 = 10 seconds
        if count == 10:
            count = 0
            database.insertMoisture(moisture_sensor.getMoisture())
            database.insertTemperature(temperature_sensor.getTemperature())

        # if 0 <= m and m < 300:
        #     result = 'Dry'
        # elif 300 <= m and m < 600:
        #     result = 'Moist'
        # else:
        #     result = 'Wet'
        # print('Moisture value: {0}, {1}'.format(m, result))

        # Control LED1
        led1 = database.selectOutput("LED1")
        GPIO.output(23, int(led1[2]))
        
        time.sleep(1)

if __name__ == '__main__':
    main()
