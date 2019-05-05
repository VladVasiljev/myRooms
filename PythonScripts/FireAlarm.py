import time
import grovepi
from firebase import firebase
import pygame
import smtplib

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  # Firebase url
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # FirebasURL on its own so we can use it throughout the script

#Connect MQ2 gas sensor to port A0 and MQ9 to port A1
gas_sensorMQ2 = 0
gas_sensorMQ9 = 1

grovepi.pinMode(gas_sensorMQ2,"INPUT")
grovepi.pinMode(gas_sensorMQ9,"INPUT")

def emailSender():#Method that allows us to send an email
    username = "123hello2020@gmail.com"#Email adress for the test account
    password = "dingatding2020"#Password for the test account
    FROM = "123hello2020@gmail.com"
    TO = ["123hello2020@gmail.com"]
    SUBJECT = "Movement Detected"
    TEXT = "Movement Detected, someone has entered your room"
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(FROM, TO, message)
        server.close()
        print ("Email Sent")       
    except:
        print ("Failed to send email")

#Method which gets the sensor values and also plays the alarm sound if the value reached by one of the sensors
#Also sending sensor values to firebase
        
def getSensorValues():
    count = 0
    while setAlarm == firebase.get(firebaseURL, '/setGasAlarm'):#Running these lines if gas alarm is set to True
        #Getting gas sensor values
        sensor_valueMQ2 = grovepi.analogRead(gas_sensorMQ2)
        sensor_valueMQ9 = grovepi.analogRead(gas_sensorMQ9)

        # Calculating gas density - large value means more dense gas
        densityMQ2 = (float)(sensor_valueMQ2 / 1024.0)
        densityMQ9 = (float)(sensor_valueMQ9 / 1024.0)
        if sensor_valueMQ2 >= 200:#If MQ2 sensor return a value of 200 of greater, we trigger things inside the if statement
            pygame.mixer.init()
            pygame.mixer.music.load("/home/pi/Desktop/2.mp3")
            pygame.mixer.music.play()
            if count == 0: #If count = 0 then we send a email
                emailSender()
                count = 1  #We set count to 1, this prevents the email being sent again
        if sensor_valueMQ9 >= 200:#If MQ9 sensor return a value of 200 of greater, we trigger things inside the if statement
            pygame.mixer.init()
            pygame.mixer.music.load("/home/pi/Desktop/2.mp3")
            pygame.mixer.music.play()
        print("sensor_valueMQ2 =", sensor_valueMQ2, " density =", densityMQ2)
        print("sensor_valueMQ9 =", sensor_valueMQ9, " density =", densityMQ9)
        firebase.put(firebaseURL, '/mq2sensorValue',sensor_valueMQ2)
        firebase.put(firebaseURL, '/mq2sensorDensity',densityMQ2)
        firebase.put(firebaseURL, '/mq9sensorValue',sensor_valueMQ9)
        firebase.put(firebaseURL, '/mq9sensorDensity',densityMQ9)
        time.sleep(.9)
    print ("Not on")


while True:
    setAlarm = "True"
    getSensorValues()
    
