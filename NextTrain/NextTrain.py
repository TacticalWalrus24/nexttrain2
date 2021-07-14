import pymysql
import csv
from os import system, name
from time import sleep
# database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="nexttrain")
# Establish cursor
cursor = connection.cursor()

def main():





class Stations:
    def __init__(self, stationID, stationName, )

class Lines:
    def __init__(self, stations[], trains[])
    self.stations = stations
class Trains:
    def __init__(self, line, location)




if __name__ == "__main__":
    main()

# commiting the connection then closing it.
connection.commit()
connection.close()
