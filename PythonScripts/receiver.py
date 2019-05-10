import sqlite3 #Importing sqlite3
from firebase import firebase #Importing python-firebase library
from datetime import datetime #Importing datetime
import time #Importing time

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  #Pointing to our Firebase through URL
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # Firebase stored in variable so we can call it any in the file

conn = sqlite3.connect('myRoomsDB.db') #Creating a connection object
c = conn.cursor() #Creating a cursor object

#Method which creates the tables if they don't exist in myRoomsDB.db
#Each table takes in two values value as BLOB and date as TEXT
def createTable():
    c.execute('CREATE TABLE IF NOT EXISTS computerRelaySwitch(value BLOB, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS mq2sensorValue(value BLOB, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS mq2sensorDensity(value BLOB, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS mq9sensorValue(value BLOB, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS mq9sensorDensity(value BLOB, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS roomTemp(value BLOB, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS roomHum(value BLOB, date TEXT)')

#Method which get values from firebase and then the values are put into tables
def enterDataToDB():
    time.sleep(3)
    
    #Getting and storing values from firebase
    computerRelaySwitch = firebase.get(firebaseURL, '/computerRelaySwitch')
    mq2sensorValue = firebase.get(firebaseURL, '/mq2sensorValue')
    mq2sensorDensity = firebase.get(firebaseURL, '/mq2sensorDensity')
    mq9sensorValue = firebase.get(firebaseURL, '/mq9sensorValue')
    mq9sensorDensity = firebase.get(firebaseURL, '/mq9sensorDensity')
    roomTemp = firebase.get(firebaseURL, '/RoomTemperature')
    roomHum = firebase.get(firebaseURL, '/RoomHumidity')
    
    date = datetime.now() #Getting current time and date
    
    #Putting the information gathered into our tables
    c.execute("INSERT INTO computerRelaySwitch(value,date)VALUES (?,?)",(computerRelaySwitch, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO mq2sensorValue(value,date)VALUES (?,?)",(mq2sensorValue, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO mq2sensorDensity(value,date)VALUES (?,?)",(mq2sensorDensity, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO mq9sensorValue(value,date)VALUES (?,?)",(mq9sensorValue, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO mq9sensorDensity(value,date)VALUES (?,?)",(mq9sensorDensity, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO roomTemp(value,date)VALUES (?,?)",(roomTemp, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO roomHum(value,date)VALUES (?,?)",(roomHum ,date.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit() #Saving changes

createTable() #Calling createTable method


while True:
    enterDataToDB() #Calling enterDataToDB method