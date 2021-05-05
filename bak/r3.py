import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(11, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(8, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(25, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(9, GPIO.OUT)           # set GPIO24 as an output   
 
try:
    while True:
#        GPIO.output(9,1)
#        GPIO.output(25,0)
        GPIO.output(11,1)
        GPIO.output(8,0)
        #print('on')
        #sleep(3)
        #GPIO.output(11,0)
        #GPIO.output(8,1)
        #print('out')
        #sleep(3)

except KeyboardInterrupt:
    GPIO.cleanup()
