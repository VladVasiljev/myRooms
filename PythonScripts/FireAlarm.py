from grovepi import *         #Importing grovePi library
import time                   #Importing time library
from firebase import firebase #Importing python-firebase library
import pygame  #Useful library which allows us to play sounds
import smtplib #Importing library which allows us to send emails from Python

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  #Pointing to our Firebase through URL
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # Firebase stored in variable so we can call it any in the file

gas_sensorMQ2 = 0 #Connect MQ2 gas sensor to port A0
gas_sensorMQ9 = 1 #Connect MQ2 gas sensor to port A1


grovepi.pinMode(gas_sensorMQ2,"INPUT") #Pin mode set to input
grovepi.pinMode(gas_sensorMQ9,"INPUT") #Pin mode set to input

dht_sensor_port = 2  # Connect the DHt sensor to port D2
dht_sensor_type = 0  # Leave at 0 if using blue-coloured sensor, change to 1 if using white coloured sensor

# Method that returns temperature value from the sensor
#Then the value is sent to firebase database
def getTemperature():  
    [temp, hum] = dht(dht_sensor_port, dht_sensor_type)
    firebase.put(firebaseURL, '/RoomTemperature',temp)
    time.sleep(1)

# Method that returns humidity value from the sensor
#Then the value is sent to firebase database
def getHumidity():
    [temp, hum] = dht(dht_sensor_port, dht_sensor_type)
    firebase.put(firebaseURL, '/RoomHumidity',hum)
    time.sleep(1)

#https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python code from the link was modified heavily
#Method that allows us to send an email from our gmail account through Python
def emailSender():
    username = "123hello2020@gmail.com" #Email Address of the account that will be used to send a email/s
    password = "dingatding2020" #Password for the account that will be sending the email
    FROM = "123hello2020@gmail.com" #Email we are sending from
    TO = ["123hello2020@gmail.com"] #Email we are sending to //Using the same as the sender email // Will work with another email
    SUBJECT = "Movement Detected" #Subject line for the email
    TEXT = "Movement Detected, someone has entered your room" #Main message for the email
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT) #Combinding all the things together
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #Server address
        server.ehlo() #Idetifying ourselves to the server
        server.starttls() #Puts the smtp conneciton into TLS mode, all SMTP commands are then encrypted
        server.login(username, password) #Logging into the account using username and password
        server.sendmail(FROM, TO, message) #Sending the email
        server.close() #Closing the connection
        print ("Email Sent")       #Printing to console that the email was sent
    except:
        print ("Failed to send email") #If email wasn't send then we will see this printed to console


#Method which sends gas sensor readings to firebase and triggers a sound if the if statements conditions are met, also an email is sent to the users email address
def getSensorValues():
    count = 0 #Setting count to zero, we can only reach here if the alarm is off
    count2 = 0 #Setting count2 to zero, we can only reach here if the alarm is off
    while setAlarm == firebase.get(firebaseURL, '/setGasAlarm'): #if setGasAlarm return True from firebase then we start readings both of the gas sensors 
        sensor_valueMQ2 = grovepi.analogRead(gas_sensorMQ2)
        sensor_valueMQ9 = grovepi.analogRead(gas_sensorMQ9)

        # Calculating gas density - large value means more dense gas
        densityMQ2 = (float)(sensor_valueMQ2 / 1024.0)
        densityMQ9 = (float)(sensor_valueMQ9 / 1024.0)
        
        if sensor_valueMQ2 >= 200:#If value is equal of exceeds the 200 mark, then we trigger a sound (Alarm) to play
            pygame.mixer.init()
            pygame.mixer.music.load("/home/pi/Desktop/2.mp3") #Location of the .mp3 file
            pygame.mixer.music.play() #playing the .mp3 file
            if count == 0: #if count is zero it means we haven't yet being send an email
                emailSender() #Calling the emailSender method
                count = 1  #We set count to 1, this prevents the email being sent again, count can be set back to zero if we disable and enabled the alarm again
        if sensor_valueMQ9 >= 200:#If MQ9 sensor return a value of 200 of greater, we trigger things inside the if statement
            pygame.mixer.init()
            pygame.mixer.music.load("/home/pi/Desktop/2.mp3") #Location of the .mp3 file
            pygame.mixer.music.play() #playing the .mp3 file
            if count2 == 0: #if count is zero it means we haven't yet being send an email
                emailSender() #Calling the emailSender method
                count2 = 1  #We set count to 1, this prevents the email being sent again, count can be set back to zero if we disable and enabled the alarm again
        print("sensor_valueMQ2 =", sensor_valueMQ2, " density =", densityMQ2) #Print values to console
        print("sensor_valueMQ9 =", sensor_valueMQ9, " density =", densityMQ9) #Print values to console
        
        #Sending sensor values and density values to firebase database
        firebase.put(firebaseURL, '/mq2sensorValue',sensor_valueMQ2)
        firebase.put(firebaseURL, '/mq2sensorDensity',densityMQ2)
        firebase.put(firebaseURL, '/mq9sensorValue',sensor_valueMQ9)
        firebase.put(firebaseURL, '/mq9sensorDensity',densityMQ9)
        getTemperature() #Calling getTemperatrue method
        getHumidity() #Calling getHumidity method
    print ("Alarm is unset") #printing this if alarm is unset to console


while True:
    setAlarm = "True"
    getSensorValues()
    
