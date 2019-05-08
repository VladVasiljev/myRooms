from gpiozero import MotionSensor
import pigpio
import time
from firebase import firebase
import pygame
import smtplib
from twilio.rest import Client

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  # Firebase url
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # FirebasURL on its own so we can use it throughout the script

#Pins that the LED lights are connected too
RED_PIN = 17# Using Pin 17 to Red LED
GREEN_PIN = 27  # Using Pin 27 to Green LED
BLUE_PIN = 22  # Using Pin 22- to Blue LED

pir = MotionSensor(4)
pi = pigpio.pi()


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
        

def set_lights(pin, brightness):
    real_brightness = int(int(brightness) * (float(255) / 255.0))
    pi.set_PWM_dutycycle(pin, real_brightness)

#Method that checks if movement was detected, if so then we flash the lights and play a sound, given that motionDetect = True
def motion():
    print("Is intruder alarm set: "+ str(firebase.get(firebaseURL, '/motionDetect')))#Printing motionDetect,checking if its ture of false 
    pir.wait_for_motion()#Waiting for motion to be detected
    print("Movement Detected: "+str(pir.wait_for_motion()))#Printing that motion was detected
    count = 0 #Setting count to 0
    while motionDetect == firebase.get(firebaseURL, '/motionDetect'):#Running these lines if motion detected and if the alarm is set
        set_lights(RED_PIN,red)
        time.sleep(0.5)
        set_lights(RED_PIN,0)
        set_lights(BLUE_PIN,blue)
        time.sleep(0.5)
        set_lights(BLUE_PIN,0)
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Desktop/1.mp3")
        pygame.mixer.music.play()
        if count == 0: #If count = 0 then we send a email
            emailSender()
            count = 1  #We set count to 1, this prevents the email being sent again, email we be sent again once the alarm is disarmed and armed again
    

while True:
   motionDetect = "True"
   red = firebase.get(firebaseURL, '/redPin')
   blue = firebase.get(firebaseURL, '/bluePin')
   motion()