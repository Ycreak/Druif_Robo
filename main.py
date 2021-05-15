# Python code for Multiple Color Detection
import numpy as np
from cv2 import cv2

from colour import Color
from processor import Processor
# Capturing video through webcam

width = 320
height = 240

webcam = cv2.VideoCapture(0)

webcam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

processor = Processor(width, height)

memory = processor.Memory('green')

box_size = 550

class Spotted_object:

    def __init__(self):
        self.location = []
        self.colour = ""
        self.size = []

def find_colour(imageFrame, hsvFrame, colour):

    mask = cv2.inRange(hsvFrame, 
        (colour.H_low, colour.S_low, colour.V_low), (colour.H_high, colour.S_high, colour.V_high))

    # Creating contour to track red color
    # contours, _ = cv2.findContours(mask,
                                        # cv2.RETR_TREE,
                                        # cv2.CHAIN_APPROX_SIMPLE)

    try:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        blob = max(contours, key=lambda el: cv2.contourArea(el))

        M = cv2.moments(blob)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        xPos = center[0]

    except (ValueError, ZeroDivisionError):
        xPos = width/2
        pass

    # kernal = np.ones((5, 5), "uint8") 
    # mask = cv2.dilate(mask, kernal)

    # for _, contour in enumerate(contours):
        # area = cv2.contourArea(contour)
        # if(area > box_size): 
            # x, y, w, h = cv2.boundingRect(contour)
            # imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                    # (x + w, y + h), 
                                    # colour.colour, 2)
            
            # # video_data.coord.append((x,y, (0,255,0)))
            # print('Coordinates: {0}-{1}'.format(x,y))              
            
            # name = str(x) + ',' + str(y)
            
            # cv2.putText(imageFrame, name, (x, y),
                        # cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        # colour.colour)  

            # spotted_object = Spotted_object()
            # spotted_object.location = (x,y)
            # spotted_object.colour = 'green'
            # spotted_object.size = (w,h)
            
            # found_object_list.append(spotted_object)

    return imageFrame, mask, xPos

class HSV_Colour():
    def __init__(self, H_low, H_high, S_low, S_high, V_low, V_high, colour=[255,255,255]):
        self.H_low = H_low
        self.H_high = H_high
        
        self.S_low = S_low
        self.S_high = S_high

        self.V_low = V_low
        self.V_high = V_high

        self.colour = colour

green = HSV_Colour(35,94,50,255,50,255, [0,255,0])
# blue = HSV_Colour(105,140,90,255,35,255, [255,0,0])
# red = HSV_Colour(56,94,71,255,15,255, [0,0,255])

run = True #False
displayWindows = True
# Start a while loop
while(1):

    found_object_list = []
    # Read Video data
    _, imageFrame = webcam.read()
    imageFrame = cv2.flip(imageFrame,-1)
    # Convert colour space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    # Draw the coloured boxes
    imageFrame, mask, xPos = find_colour(imageFrame, hsvFrame, green)
    # imageFrame = find_colour(imageFrame, hsvFrame, blue)
    # Process the frame
    if run:
        memory = processor.main(xPos, memory)
    # Show the frame (with a nice title)
    if displayWindows:
        cv2.imshow("Image Frame", imageFrame)
        cv2.imshow('mask',mask )
    print('#############################')
    # Program Termination
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
