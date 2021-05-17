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

    #FREE STATE: We are going to interpret the LEGO figure
    if memory.state == "Free":

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
            memory.state = "driving_to_goal"
            sleep(2) # Sleep to allow for LEGO withdrawal
            return memory

        # If nothing is found, just return the memory
        return memory
    
    #DRIVING TO GOAL STATE: We have a customer, let's bring him to his building
    elif memory.state == "driving_to_goal":
      print('Our destination is the {0} building.'.format(memory.goal_colour))
      
      destination_objects = [x for x in objects if x.colour == memory.goal_colour]

      #We cannot find the goal
      if not destination_objects:

        # Turn left if we have never seen our target
        if not memory.target_spotted:
          self.go_left(self.speed)

        #Drive on memory
        elif memory.spot_counter > 0:
          memory.spot_counter -= 1

          #Back to the base if we found the object
          if self.drive_toward_object(memory.last_object): #TODO: do we need if here? flex
            print('Reached the goal! Back to the base!')
            memory.state = "back_to_base"
            memory.target_spotted = False
            memory.spot_counter = 20
        
        #Start looking for the target if we looked too long
        else:
          memory.spot_counter = 20
          memory.target_spotted = False
        
      # Target in sight, drive towards it
      else:
        memory.target_spotted = True
        memory.spot_counter = -1
        self.stop() # TODO: deprecated?
        # Find the tallest object (this is most probably the building)
        tallest_building = self.Find_tallest(destination_objects)
        memory.last_object = tallest_building

        #Back to the base if we found the object
        if self.drive_toward_object(tallest_building):
          print('Reached the goal! Back to the base!')
          memory.state = "back_to_base"
          memory.target_spotted = False

    #BACK TO BASE STATE: We have reached the goal, so we can return to the base
    elif memory.state == "back_to_base":
      destination_objects = [x for x in objects if x.colour == memory.base_colour]
      
      #We cannot find the goal
      if not destination_objects:

        # Turn left if we have never seen our target
        if not memory.target_spotted:
          self.go_left(self.speed)

        #Drive on memory
        elif memory.spot_counter > 0:
          memory.spot_counter -= 1

          #Look for new lego figure if we found the base
          if self.drive_toward_object(memory.last_object): #TODO: do we need if here? flex
            print('Back at the base!')
            memory.state = "Free"
            memory.target_spotted = False
            memory.spot_counter = 20

        #Start looking for the target if we looked too long
        else:
          memory.spot_counter = 20
          memory.target_spotted = False
      
      # Target in sight, drive towards it
      else:
        base_building = self.Find_tallest(destination_objects)

        #Look for new lego figure if we found the base
        if self.drive_toward_object(base_building):
          print('Back at the base!')
          memory.state = "Free"
          memory.target_spotted = False

    else:
      print("This should not happen", memory.state)
    
    return memory

  def drive_toward_object(self, object):
    x,y = object.location
    w,h = object.size
    
    object_centre = x + (w / 2)

    print('Object location: {0}. Left: {1}, Right: {2}'.format(object_centre, self.boundary_left, self.boundary_right))
    print('Object dimensions: (x,y): ({0},{1}), (w,h): ({2},{3})'.format(x, y, w, h))

    if h > 160 and w > 85: # If it reaches top of screen, it is probably very close
      print("destination reached") # TODO: this need tweaking
      return True

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

    return False
