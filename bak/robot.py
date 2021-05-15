from gpiozero import Motor
from time import sleep
import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)

motor_left = Motor(forward=11,backward=8)
motor_right = Motor(forward=9,backward=25)

def go_left(speed):
    motor_left.backward(speed)
    motor_right.forward(speed)

def go_right(speed):
    motor_left.forward(speed)
    motor_right.backward(speed)

def go_forward(speed):
    motor_left.forward(speed)
    motor_right.forward(speed)

def go_backward(speed):
    motor_left.backward(speed)
    motor_right.backward(speed)

def stop():
    motor_left.stop()
    motor_right.stop()



try:
    while True:
        print('forward')
        go_forward(0.1)
        sleep(1)
        print('backward')
        go_backward(0.1)
        sleep(1)
        # print('left')
        # go_left(0.2)
        # sleep(2)
        # print('right')
        # go_right(0.2)
        # sleep(2)
        print('stopping')
        stop()
        GPIO.cleanup() 
        break
except KeyboardInterrupt:
    print('bye bye')

