import time
import RPi.GPIO as GPIO
from lib import Database, MoistureSensor, TemperatureSensor

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

# Create instances of components
database = Database("provil-ict.be", "gip_agritower", "agritower", "gip_2019_agritower")
moisture_sensor = MoistureSensor(0)
temperature_sensor = TemperatureSensor()

def main():
    while True:
        database.insertMoisture(moisture_sensor.getMoisture())
        database.insertTemperature(temperature_sensor.getTemperature())

        # if 0 <= m and m < 300:
        #     result = 'Dry'
        # elif 300 <= m and m < 600:
        #     result = 'Moist'
        # else:
        #     result = 'Wet'
        # print('Moisture value: {0}, {1}'.format(m, result))
        
        # database.selectOutput("POMP")

        # led1 = database.selectOutput("LED1")
        # print "status of led 1 is " + str(led1[2])

        # led2 = database.selectOutput("LED2")
        # print "status of led 2 is " + str(led1[2])

        # curs.execute("SELECT * FROM outputs ")
        # result_set = curs.fetchall()
        # for row in result_set:
        #     print "ID: " + str(row[0])
        #     print "Name: " + row[1]
        #     print "Status: " + str(row[2])
            
        #     if row[1] == "LED":
        #         GPIO.output(23, int(row[2]))
        
        time.sleep(10)

if __name__ == '__main__':
    main()
