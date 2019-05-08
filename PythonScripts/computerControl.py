from grovepi import *
import time
from firebase import firebase

firebase = firebase.FirebaseApplication('https://myrooms-2019iot.firebaseio.com/')  # Firebase url
firebaseURL = 'https://myrooms-2019iot.firebaseio.com/'  # FirebasURL on its own so we can use it throughout the script

relay = 3
pinMode(relay,"OUTPUT")

def relayControl():
    computerRelaySwitch = firebase.get(firebaseURL, '/computerRelaySwitch')
    if computerRelaySwitch == 1:
        digitalWrite(relay,1)
        time.sleep(1)
        digitalWrite(relay,0)
        firebase.put(firebaseURL, '/computerRelaySwitch',0)
        
while True:
   relayControl()