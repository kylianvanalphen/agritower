import MySQLdb
from datetime import datetime

class Database:
    def __init__(self, host, username, password, database):
        self.db = MySQLdb.connect(host, username, password, database)
        self.cursor = self.db.cursor()
    
    def insertMoisture(self, value):
        current_dt = datetime.now()

        try:
            self.cursor.execute("INSERT INTO moistureSensor (datum, waarde) VALUES (%s,%s)", (current_dt.strftime("%Y/%m/%d %H:%M:%S"), str(value)))
            self.db.commit()
        except:
            print "Error while inserting moisture sensor data"
            self.db.rollback()

    def insertTemperature(self, value):
        current_dt = datetime.now()

        try:
            self.cursor.execute("INSERT INTO temperatureSensor (datum, waarde) VALUES (%s,%s)", (current_dt.strftime("%Y/%m/%d %H:%M:%S"), str(value)))
            self.db.commit()
        except:
            print "Error while inserting temperature sensor data"
            self.db.rollback()

    def selectOutput(self, name):
        self.cursor.execute("SELECT * FROM outputs WHERE name = %s", name)
        return curs.fetchone()