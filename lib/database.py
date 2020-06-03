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
        self.cursor.execute("SELECT * FROM outputs WHERE name = %s", (name,))
        return self.cursor.fetchone()

    def moveMoistureArchive(self):
        try:
            self.cursor.execute("INSERT INTO archiveMoistureSensor SELECT id, datum, waarde FROM moistureSensor WHERE datum <= DATE_SUB(SYSDATE(), INTERVAL 2 DAY)")
            self.cursor.execute("DELETE FROM moistureSensor WHERE datum <= DATE_SUB(SYSDATE(), INTERVAL 2 DAY)")
            self.db.commit()
        except:
            print "Error while moving moisture sensor records to archive"
            self.db.rollback()

    def moveTemperatureArchive(self):
        try:
            self.cursor.execute("INSERT INTO archiveTemperatureSensor SELECT id, datum, waarde FROM temperatureSensor WHERE datum <= DATE_SUB(SYSDATE(), INTERVAL 2 DAY)")
            self.cursor.execute("DELETE FROM temperatureSensor WHERE datum <= DATE_SUB(SYSDATE(), INTERVAL 2 DAY)")
            self.db.commit()
        except:
            print "Error while moving temperature sensor records to archive"
            self.db.rollback()

    def insertStatus(self, value, name): 
         current_dt = datetime.now()

        try:
            self.cursor.execute("INSERT INTO archiveOutputStatus (datum, waarde, output) VALUES (%s,%s, %s)", (current_dt.strftime("%Y/%m/%d %H:%M:%S"), str(value), str(name)))
            self.db.commit()
        except:
            print "Error while inserting status"
            self.db.rollback()