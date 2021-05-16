from playsound import playsound
import time

# Motor
from gpiozero import Motor
from time import sleep
import RPi.GPIO as GPIO  


class Goal:
  def __init__(self, colour):

    # self.goal = goal
    self.colour = colour

class Processor:
  def __init__(self, frame_width, frame_height):

    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup() 

    self.motor_left = Motor(forward=20,backward=26)
    self.motor_right = Motor(forward=16,backward=19)
    
    self.width = frame_width
    self.height = frame_height

    # Vacancy of the ride
    self.free = False
    self.speed = 0.15
    self.offset = 75

    self.boundary_left = self.width/2 - self.offset
    self.boundary_right = self.width/2 + self.offset

  def go_left(self, speed):
    self.motor_left.backward(speed)
    # self.motor_right.forward(speed)

  def go_right(self, speed):
    # self.motor_left.forward(speed)
    self.motor_right.backward(speed)

  def go_forward(self, speed):
    self.motor_left.forward(speed)
    self.motor_right.forward(speed)

  def go_backward(self, speed):
    self.motor_left.backward(speed)
    self.motor_right.backward(speed)

  def stop(self):
    self.motor_left.stop()
    self.motor_right.stop()

  def drive(self, right, left):
    self.motor_left.forward(left)
    self.motor_right.forward(right)

  def Find_largest(self, objects, colour):
    
    biggest = 0

    for object in objects:
      if object.colour == colour:    
        w,h = object.size

        if (w*h) > biggest:
          biggest_object = object
          biggest = w*h

    try:
      x, y = biggest_object.location
      w, h = biggest_object.size

      # Find the centre of the object
      biggest_object.centre = x + (w / 2)

      return biggest_object

    except:
      return None

  def Find_tallest(self, objects):
    tallest = 0

    for object in objects:
      w,h = object.size

      if h > tallest:
        tallest_object = object
        tallest = h

    return tallest_object

  def main(self, memory, objects):   
    """
    1. Search for LEGO Figures.
        Find Yellow and the color underneath
    2. Find the destination
        Find the color and check if not yellow

    Args:
        objects ([type]): [description]
    """    

    # Stop motors and await new orders
    self.stop()

    if memory.free:
      ''' We are going to interpret the LEGO figure and bring him to his destination '''

      # If we cannot find objects, return memory
      if not objects:
        print('No objects found!')
        self.stop()
        return memory

      else:
        yellow_objects = [x for x in objects if x.colour == 'yellow']
        if yellow_objects:
          lego_head = self.Find_largest(yellow_objects, 'yellow')
          # Find the location of the neck of the figure, where it should meet a shirt
          lego_neck = lego_head.location[1] + lego_head.size[1] # head.x + head.height
        else:
          print('No LEGO figure found')
          return memory
        # Now check if there is an object under the lego head, which should be a shirt
        for object in objects:
          if(object.location[1] in range(lego_neck - 20, lego_neck + 20)) and object.colour != 'yellow':
            print('LEGO FIGURE with shirt colour {0}'.format(object.colour))
            # Set goal colour and vacancy status
            memory.goal_colour = object.colour
            memory.free = False
            sleep(2) # Sleep to allow for LEGO withdrawal
            return memory

        # If nothing is found, just return the memory
        return memory
    
    else:
      ''' We have a customer, let's bring him to his building '''
      print('Our destination is the {0} building.'.format(memory.goal_colour))
      
      destination_objects = [x for x in objects if x.colour == memory.goal_colour]
      # print('dest_obj', destination_objects)

      if not destination_objects:
        # No destination object in sight
        print('No objects, going right')
        self.go_right(self.speed)
      
      else:
        self.stop()
        # Find the tallest object (this is most probably the building)
        tallest_building = self.Find_tallest(objects)
        self.drive_toward_object(tallest_building)

      return memory

  def drive_toward_object(self, object):
    x,y = object.location
    w,h = object.size
    
    object_centre = x + (w / 2)

    print('Object location: {0}. Left: {1}, Right: {2}'.format(object_centre, self.boundary_left, self.boundary_right))

    # if y < 20: # If it reaches top of screen, it is probably very close
    #   print("destination reached") # TODO: this need tweaking
    #   exit(0)
    #   # return True
    if object_centre > self.boundary_right: # Try to centre the object
      print("drive right") # i cant think mirrored
      self.go_right(self.speed)

    elif object_centre < self.boundary_left:
      print("drive left")
      self.go_left(self.speed)

    else:
      print("drive forward")
      self.go_forward(self.speed)
      # sleep(0.2)
      # self.stop()
    # print("Object Centre: {0}, W_l: {1}, W_r: {2}".format(x, (self.frame_width / 2 - offset), (self.frame_width / 2 + offset)))

    # return False
