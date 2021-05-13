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

    self.motor_left = Motor(forward=11,backward=8)
    self.motor_right = Motor(forward=9,backward=25)
    
    self.frame_width = frame_width
    self.frame_height = frame_height

    # Vacancy of the ride
    self.free = False

  def go_left(self, speed):
    self.motor_left.backward(speed)
    self.motor_right.forward(speed)

  def go_right(self, speed):
    self.motor_left.forward(speed)
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


  class Memory:
    def __init__(self, colour):

      # self.goal = goal
      self.goal_colour = colour  

  def Check_largest(self, object, biggest):
    w,h = object.size
    # Assignment
    biggest_object = object


    if (w+h) > biggest:
      biggest_object = object
      biggest = w+h

    return biggest, biggest_object


  def main(self, objects, memory):   
    """
    1. Search for LEGO Figures.
        Find Yellow and the color underneath
    2. Find the destination
        Find the color and check if not yellow

    Args:
        objects ([type]): [description]
    """    
    

    # TODO: drive around objects!
    goal_colour = 'green'

    if self.free: 
      # Find a LEGO figure to pickup
 
      # biggest = 0
      biggest_yellow = 0

      new_objects = []
      yellow_found = False

      # Try, because we cannot always find an object (maybe check if objects is filled)
      if objects:

          for object in objects:
              # Find the biggest yellow item on screen
              if object.colour == 'yellow':
                biggest_yellow, biggest_yellow_object = self.Check_largest(object, biggest_yellow)
                yellow_found = True
              # If it is not yellow, add it to a new list
              else:
                new_objects.append(object)

              # elif object.colour == 'red':
              #   biggest_red, biggest_red_object = self.Check_largest(object, biggest_red)

          # Make the old objects list the new one (now without yellow)
          objects = new_objects

          if yellow_found:
            # Find shirt
            head_lower = biggest_yellow_object.location[1] + biggest_yellow_object.size[1]

            # Find the shirt colour
            if objects:



              for object in objects:
                object_top = object.location[1]
                if(object_top in range(head_lower - 20, head_lower + 20)):
                  print('LEGO FIGURE with shirt colour {0}'.format(object.colour))
                  if self.drive_toward_object(object):
                    # Now the LEGO figure has been reached
                    # playsound("arrived.ogg")    # Play the sound effect
                    # time.sleep(2.0)             # Wait a few seconds
                    self.free = False           # Now we are occupied
                    goal_colour = object.colour # Set the colour to our goal TODO: i want this in an object
                    break                       # Break out of the loop
            else:
              print('Cannot find shirt colour')


          else:
            print('No LEGO found, continuing driving')
            # Continue driving
      
      else:
          print('No objects found in view')
          # Continue driving

    else: # WE ARE FINDING A BUILDING HERE
      self.stop()

      # We are occupied, find the destination
      # print("Where is the {0} building?".format(goal_colour))
      if objects:
        print('hi')
        # Find one with the correct colour that is not a LEGO figure

        # no_yellow = True
        # # Dirty hack, we dont want yellow in this frame
        # for object in objects:
        #   if object.colour == 'yellow':
        #     no_yellow = False
        #     break

        # if no_yellow:
        for object in objects:
          if object.colour == goal_colour: # This assumes only one goal color remains (maybe find biggest)
              self.drive_toward_object(object)
              break                       # Break out of the loop
                # # Now the LEGO figure has been reached
                # # playsound("arrived.ogg")    # Play the sound effect
                # time.sleep(3.0)             # Wait a few seconds
                # self.free = True            # Now we are occupied
                # goal_colour = 'none'       # Set the colour to our goal TODO: i want this in an object
                # exit(0)
          else:
            print('Goal not found')
            # Continue driving
          pass
      else:
        print("No objects found.")
        # self.go_left(0.15)
        # Continue driving

    return memory


  def drive_toward_object(self, object):
    x, y = object.location
    w,h = object.size

    # Find the centre of the object
    x = x + (w / 2)

    print(x, y)
    offset = 150

    if y < 20: # If it reaches top of screen, it is probably very close
      print("destination reached") # TODO: this need tweaking
      exit(0)
      # return True
    elif x > (self.frame_width / 2 + offset): # Try to centre the object
      print("drive right") # i cant think mirrored
      self.go_right(0.2)
      # sleep(0.2)
      # self.stop()
    elif x < (self.frame_width / 2 - offset):
      print("drive left")
      self.go_left(0.2)
      # sleep(0.2)
      # self.stop()
    else:
      print("drive forward")
      self.go_forward(0.2)
      # sleep(0.2)
      # self.stop()
    print("X: {0}, W_r: {1}, W_l: {2}".format(x, (self.frame_width / 2 + offset), (self.frame_width / 2 - offset)))

    # COMMENT THIS FOR DEMONSTRATION
    sleep(0.1)
    self.stop()

    # return False