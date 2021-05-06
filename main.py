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


class Video_data:
    
    def __init__(self):

        self.coord = []
    
class Spotted_object:

    def __init__(self):
        self.location = []
        self.colour = ""
        self.size = []


# Start a while loop
while(1):

    found_object_list = []

    video_data = Video_data()

    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()

    imageFrame = cv2.flip(imageFrame,-1)

    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    def find_colour(imageFrame, hsvFrame, name, colour, colour_lower, colour_upper):

        colour_lower_array = np.array(colour_lower, np.uint8)
        colour_upper_array = np.array(colour_upper, np.uint8)
        # red_lower = np.array([136, 87, 111], np.uint8)
        # red_upper = np.array([180, 255, 255], np.uint8)    
        mask = cv2.inRange(hsvFrame, colour_lower_array, colour_upper_array)

        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
    
        colour.reverse() #(bgr)

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        kernal = np.ones((5, 5), "uint8")
        
        # For red color
        mask = cv2.dilate(mask, kernal)
        # res_colour = cv2.bitwise_and(imageFrame, imageFrame, 
        #                         mask = mask)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > box_size): 
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                        (x + w, y + h), 
                                        colour, 2)
                
                # video_data.coord.append((x,y, colour))
                # print('Coordinates: {0}-{1}'.format(x,y))              
                # cv2.putText(imageFrame, name, (x, y),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                #             colour)  

                spotted_object = Spotted_object()
                spotted_object.location = (x,y)
                spotted_object.colour = name
                spotted_object.size = (w,h)
                
                found_object_list.append(spotted_object)

        return imageFrame

    # Set range for red color and 
    # define mask
    red = [255,0,0]
    green = [0,255,0]
    blue = [0,0,255]
    yellow = [255,255,0]
    black = [0,0,0]

    red_lower = [0, 180, 180]
    red_upper = [255, 255, 255]

    green_lower = [25, 100, 72]
    green_upper = [90, 255, 200]

    blue_lower = [110,50,50]
    blue_upper = [130,255,255]

    yellow_lower = [20,100,100]
    yellow_upper = [30,255,255]

    black_lower = [10, 100, 50]
    black_upper = [50, 255, 255]

    # imageFrame = find_colour(imageFrame, hsvFrame, 'red', red, red_lower, red_upper)
    imageFrame = find_colour(imageFrame, hsvFrame, 'green', green, green_lower, green_upper)
    # imageFrame = find_colour(imageFrame, hsvFrame, 'blue', blue, blue_lower, blue_upper)
    # imageFrame = find_colour(imageFrame, hsvFrame, 'yellow', yellow, yellow_lower, yellow_upper)
    # imageFrame = find_colour(imageFrame, hsvFrame, 'black', black, black_lower, black_upper)

    memory = processor.main(found_object_list, memory) 

    # video_data.coord = []

    # Program Termination
    # cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)

    print('#############################')

    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break