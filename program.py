# import MySQLdb
import math
import sys
import time
from grove.adc import ADC
from datetime import datetime
import os
import glob
import RPi.GPIO as GPIO
from lib import Database

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

# db = MySQLdb.connect("provil-ict.be","gip_agritower","agritower","gip_2019_agritower")
# curs=db.cursor()

database = Database("provil-ict.be", "gip_agritower", "agritower", "gip_2019_agritower")

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


class GroveMoistureSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def moisture(self):
        '''
        Get the moisture strength value/voltage

        Returns:
            (int): voltage, in mV
        '''
        value = self.adc.read_voltage(self.channel)
        return value

Grove = GroveMoistureSensor



def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
    

def main():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = 0

    sensor = GroveMoistureSensor(pin)

    print('Detecting moisture...')
    while True:
        m = sensor.moisture

        database.insertMoisture(m)
        database.insertTemperature(read_temp())

        # current_dt = datetime.now()

        # try:
            # print "temp is"
            # print read_temp()
            # curs.execute("INSERT INTO moistureSensor (datum, waarde)  VALUES (%s,%s)", (current_dt.strftime("%Y/%m/%d %H:%M:%S"), str(m)))
            # curs.execute("INSERT INTO temperatureSensor (datum, waarde)  VALUES (%s,%s)", (current_dt.strftime("%Y/%m/%d %H:%M:%S"), str(read_temp())))
            # db.commit()
            # database.insertMoisture(waarde)
            # print "data commited"
        # except:
            # print "error"
            # db.rollback()

        # if 0 <= m and m < 300:
        #     result = 'Dry'
        # elif 300 <= m and m < 600:
        #     result = 'Moist'
        # else:
        #     result = 'Wet'
        # print('Moisture value: {0}, {1}'.format(m, result))
        
        # database.selectOutput("POMP")

        led1 = database.selectOutput("LED1")
        print "status of led 1 is " + str(led1[2])

        led2 = database.selectOutput("LED2")
        print "status of led 2 is " + str(led1[2])

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
