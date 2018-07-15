# binfulltext is IoT project to use a raspberry pi3 to sense a full recycling bin using an ultrasonic distance sensor and then send a text message alert using twilio 
#Libraries to use GPIO and be able to time signal and twilio api to enable text messages
import RPi.GPIO as GPIO
import time
import twilio
import twilio.rest
from twilio.rest import Client

# Account SID from twilio.com/console
account_sid = "your acccount sid" 
# Auth Token from twilio.com/console
auth_token  = "your auth token"

client = Client(account_sid, auth_token)

#Set up the pins for the sensors
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
#Turn off warnings
GPIO.warnings(False)

#set GPIO Pins on Raspberry Pi3
GPIO_TRIGGER= 23
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

while True:
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance= TimeElapsed * 17510
    #round to two decimals 
    distance= round(distance,2)
    
#Check whether the bin is full
if distance >=20:
    #Print how much space is left in the bin if it is not yet full
    print ("Bin Not Full: ",distance,"cm of space left")
    # Wait for a while until checking on the distance again
    time.sleep(10)    
else:
    #Print only when bin is full
    print ("Bin FULL: ",distance,"cm of space left, text alert sent")                     
    message = client.messages.create(
        to="+14083861706", 
        from_="+14086179281",
        body="The paper bin on the 16th Floor is FULL!")
    print (message.sid)
    # Wait for a minute until checking on the distance again and sending another text
    time.sleep(60)