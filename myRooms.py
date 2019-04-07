from gpiozero import MotionSensor
import pigpio
import time

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  # Firebase url
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # FirebasURL on its own so we can use it throughout the script

RED_PIN = 17# Using Pin 17 to Red LED
GREEN_PIN = 27  # Using Pin 27 to Green LED
BLUE_PIN = 22  # Using Pin 22- to Blue LED

pir = MotionSensor(4)
motionDetect = firebase.get(firebaseURL, '/motionDetect')
pi = pigpio.pi()

def set_lights(pin, brightness):
    real_brightness = int(int(brightness) * (float(255) / 255.0))
    pi.set_PWM_dutycycle(pin, real_brightness)
    
def motion():
    pir.wait_for_motion()
    print("You moved"+ str(motionDetect))
    #motionDetect = True
    while motionDetect == True:
        time.sleep(0.5)
        set_lights(RED_PIN,255)
        time.sleep(0.5)
        set_lights(RED_PIN,0)

    


while True:
   motion()