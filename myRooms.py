from gpiozero import MotionSensor
import pigpio
import time
from firebase import firebase
import pygame

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  # Firebase url
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # FirebasURL on its own so we can use it throughout the script

#Pins that the LED lights are connected too
RED_PIN = 17# Using Pin 17 to Red LED
GREEN_PIN = 27  # Using Pin 27 to Green LED
BLUE_PIN = 22  # Using Pin 22- to Blue LED

pir = MotionSensor(4)
pi = pigpio.pi()

def set_lights(pin, brightness):
    real_brightness = int(int(brightness) * (float(255) / 255.0))
    pi.set_PWM_dutycycle(pin, real_brightness)
    
def motion():
    print("Is intruder alarm set: "+ str(firebase.get(firebaseURL, '/motionDetect')))
    pir.wait_for_motion()
    print("Movement Detected: "+str(pir.wait_for_motion()))
    #motionDetect = True
    while motionDetect == firebase.get(firebaseURL, '/motionDetect'):
        set_lights(RED_PIN,red)
        time.sleep(0.5)
        set_lights(RED_PIN,0)
        set_lights(BLUE_PIN,blue)
        time.sleep(0.5)
        set_lights(BLUE_PIN,0)
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Desktop/1.mp3")
        pygame.mixer.music.play()
    

while True:
   motionDetect = "True"
   red = firebase.get(firebaseURL, '/redPin')
   blue = firebase.get(firebaseURL, '/bluePin')
   motion()