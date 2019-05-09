from grovepi import *         #Importing grovePi library
import time                   #Importing time library
from firebase import firebase #Importing python-firebase library
from threading import Thread  #Importing Treading from Thread

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  #Pointing to our Firebase through URL
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # Firebase stored in variable so we can call it any in the file

relay = 3 #Connect relay switch to port D3
pinMode(relay,"OUTPUT") #Pin mode set to output

#Method for controlling the relay switch
#How the method works?
#Get and store values from firebase database to computerRelaySwitch, values can be 0 = off , 1 = on
#If statement which checks if value is equalTo 1, if so then we switch the relay switch on and keep it on for 1 second
#Then we switch the relay switch off and set the value of computerRelaySwitch to 0 in Firebase
def relayControl():
    computerRelaySwitch = firebase.get(firebaseURL, '/computerRelaySwitch')
    if computerRelaySwitch == 1:
        digitalWrite(relay,1)
        time.sleep(1)
        digitalWrite(relay,0)
        firebase.put(firebaseURL, '/computerRelaySwitch',0)
while True:
    time.sleep(2)
    publisher_thread = Thread(target=relayControl)
    publisher_thread.start()