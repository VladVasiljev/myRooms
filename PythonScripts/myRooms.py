from gpiozero import MotionSensor #Importing motionSensor library from gpiozero
import pigpio #Importing piggpio used fro lights
import time #Importing time
from firebase import firebase #Importing python-firebase library
import pygame  #Useful library which allows us to play sounds
import smtplib #Importing library which allows us to send emails from Python
from twilio.rest import Client #Importaing Twilio library that allows us to send SMS to our phone
import configTwilio #importing configTwilio.py file to this class

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  #Pointing to our Firebase through URL
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # Firebase stored in variable so we can call it any in the file


RED_PIN = 17 # Using Pin 17 to Red LED
GREEN_PIN = 27  # Using Pin 27 to Green LED
BLUE_PIN = 22  # Using Pin 22- to Blue LED

pir = MotionSensor(4) #Connect motion sensor to Pin 4 (5v power)
pi = pigpio.pi()

#Method which sends a SMS to users mobile number
def sendSMSToMobile(body):
	client = Client(configTwilio.account_sid, configTwilio.auth_token) #Getting account_sid and auth_token info from configTwilio.py file and storing that information in client varaible
	#Creating a message which also has the client information
	#sms_to = what phone number we are going to send info to
	#sms_from = which phone number will be used to send the message Twilio provides the number.
	message = client.messages.create(
		to = configTwilio.sms_to,
		from_ = configTwilio.sms_from_,
		body = body)
	print (message.sid)

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
        set_lights(RED_PIN,red) #Setting light colour for Red
        time.sleep(0.5)
        set_lights(RED_PIN,0)
        set_lights(BLUE_PIN,blue) #Setting lights colour for Blue
        time.sleep(0.5)
        set_lights(BLUE_PIN,0)
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Desktop/1.mp3") #Location of the .mp3 file
        pygame.mixer.music.play() #playing the .mp3 file
        if count == 0: #if count is zero it means we haven't yet being send an email
            emailSender() #Calling the emailSender method
            #body = "Oh no, someone must of entered your room, the motion sensor has been trigged. Don't worry the alarm is sounding and the lights are flashing" #Message for the sms
            #sendSMSToMobile(body) #Calling sendSMSToMobile method with body, which is the message that will be sent to the user.
            count = 1  #We set count to 1, this prevents the email being sent again, count can be set back to zero if we disable and enabled the alarm again
            
while True:
   motionDetect = "True"
   red = firebase.get(firebaseURL, '/redPin')
   blue = firebase.get(firebaseURL, '/bluePin')
   motion()
