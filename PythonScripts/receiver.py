import sqlite3 #Importing sqlite3
from firebase import firebase #Importing python-firebase library
from datetime import datetime

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  #Pointing to our Firebase through URL
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # Firebase stored in variable so we can call it any in the file

conn = sqlite3.connect('myRoomsDB.db') 
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS motionDetect(value TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS computerRelaySwitch(value TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS mq2sensorValue(value TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS mq2sensorDensity(value TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS mq9sensorValue(value TEXT, date TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS mq9sensorDensity(value TEXT, date TEXT)')


def enterDataToDB():
    computerRelaySwitch = firebase.get(firebaseURL, '/computerRelaySwitch')
    check = computerRelaySwitch
    mq2sensorValue = firebase.get(firebaseURL, '/mq2sensorValue')
    mq2sensorDensity = firebase.get(firebaseURL, '/mq2sensorDensity')
    mq9sensorValue = firebase.get(firebaseURL, '/mq9sensorValue')
    mq9sensorDensity = firebase.get(firebaseURL, '/mq9sensorDensity')
    date = datetime.now() 
    c.execute("INSERT INTO motionDetect(value,date)VALUES (?,?)",(motionDetect, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO computerRelaySwitch(value,date)VALUES (?,?)",(computerRelaySwitch, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO mq2sensorValue(value,date)VALUES (?,?)",(mq2sensorValue, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO mq2sensorDensity(value,date)VALUES (?,?)",(mq2sensorDensity, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO mq9sensorValue(value,date)VALUES (?,?)",(mq9sensorValue, date.strftime('%Y-%m-%d %H:%M:%S')))
    c.execute("INSERT INTO mq9sensorDensity(value,date)VALUES (?,?)",(mq9sensorDensity, date.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()

create_table()


while True:
    enterDataToDB()