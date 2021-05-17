# Python code for Multiple Color Detection
import numpy as np
from cv2 import cv2

from colour import Color
from processor import Processor
# Capturing video through webcam

import sys

width = 320
height = 240

webcam = cv2.VideoCapture(0)

webcam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

processor = Processor(width, height)

box_size = 200

class Spotted_object:
    # Object to save a spotted object in
    def __init__(self):
        self.location = []
        self.colour = ""
        self.size = []

def find_colour(imageFrame, hsvFrame, colour):

    mask = cv2.inRange(hsvFrame, 
        (colour.H_low, colour.S_low, colour.V_low), (colour.H_high, colour.S_high, colour.V_high))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > box_size): 
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                    (x + w, y + h), 
                                    colour.colour, 2)
                           
            # cv2.putText(imageFrame, name, (x, y),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.0,
            #             colour.colour)  

            spotted_object = Spotted_object()
            spotted_object.location = (x,y)
            spotted_object.colour = colour.name
            spotted_object.size = (w,h)
            
            found_object_list.append(spotted_object)

    return imageFrame, mask

class HSV_Colour():
    # Object to save a HSV colour in
    def __init__(self, H_low, H_high, S_low, S_high, V_low, V_high, colour, name):
        self.H_low = H_low
        self.H_high = H_high
        
        self.S_low = S_low
        self.S_high = S_high

        self.V_low = V_low
        self.V_high = V_high

        self.colour = colour
        self.name = name

class Memory:
    def __init__(self):
        self.free = True
        self.goal_colour = 'blue' 
        self.target_spotted = False
        self.spot_counter = -1
        fake_object = Spotted_object()
        fake_object.location = (-1,-1)
        fake_object.colour = "FAKE"
        fake_object.size = (-1,-1)
        self.last_object = fake_object

        self.back_to_base = False
        self.base_colour = 'green'

# Colours in HSV and BGR
green = HSV_Colour(35,94,135,255,39,255, [0,255,0], 'green')
blue = HSV_Colour(105,140,90,255,35,255, [255,0,0], 'blue')
red = HSV_Colour(169,180,55,255,51,255, [0,0,255], 'red')
yellow = HSV_Colour(21,40,50,255,90,255, [0,255,255], 'yellow')

run = False
displayWindows = True
memory = Memory()

try:
    if sys.argv[1] == 'run':
        run = True
except:
    pass

# Start a while loop
while(1):

    found_object_list = []
    # Read Video data
    _, imageFrame = webcam.read()
    imageFrame = cv2.flip(imageFrame,-1)
    # Convert colour space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    # Draw the coloured boxes
    imageFrame, mask = find_colour(imageFrame, hsvFrame, green)
    imageFrame, mask = find_colour(imageFrame, hsvFrame, red)
    imageFrame, mask = find_colour(imageFrame, hsvFrame, blue)
    imageFrame, mask = find_colour(imageFrame, hsvFrame, yellow)
    # Process the frame
    if run:
        memory = processor.main(memory, found_object_list)
    # Show the frame
    if displayWindows:
        cv2.imshow("Image Frame", imageFrame)
        # cv2.imshow('mask',mask )
    print('#############################')
    # Program Termination
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
