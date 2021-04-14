import numpy as np
from cv2 import cv2

class Webcam0:

  def find_colour(self, imageFrame, hsvFrame, name, colour, colour_lower, colour_upper):

      colour_lower_array = np.array(colour_lower, np.uint8)
      colour_upper_array = np.array(colour_upper, np.uint8)
      # red_lower = np.array([136, 87, 111], np.uint8)
      # red_upper = np.array([180, 255, 255], np.uint8)    
      mask = cv2.inRange(hsvFrame, colour_lower_array, colour_upper_array)

      # Creating contour to track red color
      contours, hierarchy = cv2.findContours(mask,
                                          cv2.RETR_TREE,
                                          cv2.CHAIN_APPROX_SIMPLE)
  
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
          if(area > 300):
              x, y, w, h = cv2.boundingRect(contour)
              imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                      (x + w, y + h), 
                                      (255,0,0), 2)
              # print('Coordinates: {0}-{1}'.format(x,y))              
              cv2.putText(imageFrame, name, (x, y),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                          colour.reverse())  # For some reason, this colour should be encoded in BRG instead of RGB

      return imageFrame



  def __init__(self):  

    webcam = cv2.VideoCapture(0)

    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()

    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and 
    # define mask
    red = [255,0,0]
    green = [0,255,0]
    blue = [0,0,255]

    red_lower = [0, 180, 180]
    red_upper = [255, 255, 255]

    green_lower = [25, 100, 72]
    green_upper = [90, 255, 200]

    blue_lower = [110,50,50]
    blue_upper = [130,255,255]

    imageFrame = self.find_colour(imageFrame, hsvFrame, 'Red Colour', red, red_lower, red_upper)
    imageFrame = self.find_colour(imageFrame, hsvFrame, 'Green Colour', green, green_lower, green_upper)
    imageFrame = self.find_colour(imageFrame, hsvFrame, 'Blue Colour', blue, blue_lower, blue_upper)

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
    # if cv2.waitKey(10) & 0xFF == ord('q'):
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     break
