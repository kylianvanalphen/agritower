import MySQLdb

db = MySQLdb.connect("provil-ict.be","gip_agritower","agritower","gip_2019_agritower")
curs=db.cursor()

class Database: