# Python code for Multiple Color Detection
import numpy as np
from cv2 import cv2

from colour import Color
from processor import Processor
# Capturing video through webcam

frame_width = 800
frame_height = 600

webcam = cv2.VideoCapture(0)

webcam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

processor = Processor(frame_width, frame_height)

memory = processor.Memory('green')

box_size = 550

class Spotted_object:
    # Object to save a spotted object in
    def __init__(self):
        self.location = []
        self.colour = ""
        self.size = []

def find_colour(imageFrame, hsvFrame, colour):
    # Finds the given colour on the frame and draws a rectangle around it

    frame_threshold = cv2.inRange(hsvFrame, 
        (colour.H_low, colour.S_low, colour.V_low), (colour.H_high, colour.S_high, colour.V_high))

    # Creating contour to track red color
    contours, _ = cv2.findContours(frame_threshold,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)

    kernal = np.ones((5, 5), "uint8") 
    frame_threshold = cv2.dilate(frame_threshold, kernal)

    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(500<area<5000): 
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                    (x + w, y + h), 
                                    colour.colour, 2)
            
            # video_data.coord.append((x,y, (0,255,0)))
            # print('Coordinates: {0}-{1}'.format(x,y))              
            
            # name = str(x) + ',' + str(y)
            
            # cv2.putText(imageFrame, name, (x, y),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.0,
            #             colour.colour)  

            spotted_object = Spotted_object()
            spotted_object.location = (x,y)
            spotted_object.colour = 'green'
            spotted_object.size = (w,h)
            
            found_object_list.append(spotted_object)

    return imageFrame

class HSV_Colour():
    # Object to save a HSV colour in
    def __init__(self, H_low, H_high, S_low, S_high, V_low, V_high, name, colour=[255,255,255]):
        self.H_low = H_low
        self.H_high = H_high
        
        self.S_low = S_low
        self.S_high = S_high

        self.V_low = V_low
        self.V_high = V_high

        self.colour = colour
        self.name = name

green = HSV_Colour(35,94,50,255,50,255, [0,255,0])
blue = HSV_Colour(105,140,90,255,35,255, [255,0,0])
# red = HSV_Colour(56,94,71,255,15,255, [0,0,255])

# Start a while loop
while(1):
    
    start = time.time()
    
    found_object_list = []
    # Read Video data
    _, imageFrame = webcam.read()
    imageFrame = cv2.flip(imageFrame,-1)
    # Convert colour space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    # Draw the coloured boxes
    imageFrame = find_colour(imageFrame, hsvFrame, green)
    # imageFrame = find_colour(imageFrame, hsvFrame, blue)
    # Process the frame
    memory = processor.main(found_object_list, memory) 
    # Show the frame (with a nice title)
    # cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
    print('#############################')
    # Program Termination
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
