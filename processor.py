import time

# Google text to speech
from gtts import gTTS

# IO for mp3 file handling
from io import BytesIO

# Motor
from gpiozero import Motor
from time import sleep
import RPi.GPIO as GPIO  

# Imports for playing audio
from pydub import AudioSegment
from pydub.playback import play

class Processor:
  """ Main class that implements the working of the robot
  """
  def __init__(self, frame_width, frame_height):

    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup() 

    # Initialize motors
    self.motor_left = Motor(forward=20, backward=26)
    self.motor_right = Motor(forward=16, backward=19)
    
    # Set defaults
    self.width = frame_width
    self.height = frame_height

    # Amount of frames to drive backwards
    self.drive_back_counter_default = 20
    self.speed = 0.18 # Motor speed (percentage)
    self.offset = 75  # Offset to determine boundaries

    self.boundary_left = self.width / 2 - self.offset   # Between it is center
    self.boundary_right = self.width / 2 + self.offset

    """ Methods to move the robot in certain directions
    """
  def go_left(self, speed):
    self.motor_left.backward(speed)
    self.motor_right.forward(speed - 0.05)

  def go_right(self, speed):
    self.motor_left.forward(speed - 0.05)
    self.motor_right.backward(speed)

  def go_forward(self, speed):
    self.motor_left.forward(speed - 0.05)
    self.motor_right.forward(speed- 0.05)

  def go_backward(self, speed):
    self.motor_left.backward(speed)
    self.motor_right.backward(speed)

  def stop(self):
    """ Attempt to stop the motors
    """    
    self.motor_left.stop()
    self.motor_right.stop()

  def find_largest(self, objects, colour):
    """ Attempt to find the largest object of a certain color

    Args:
        objects (list): identified objects
        colour (HSV_COLOR): color to search for

    Returns:
        Object: The biggest object of that color
    """    
    biggest = 0

    for object in objects:
      if object.colour == colour:    
        w, h = object.size

        if (w * h) > biggest:
          biggest_object = object
          biggest = w*h

    try:
      x, _ = biggest_object.location
      w, h = biggest_object.size

      # Find the centre of the object
      biggest_object.centre = x + (w / 2)
      return biggest_object

    except:
      return None

  def Find_tallest(self, objects):
    """Find the tallest off all objects

    Args:
        objects (list): list of objects

    Returns:
        Object: The tallest object
    """    
    tallest = 0

    for object in objects:
      w,h = object.size

      if h > tallest:
        tallest_object = object
        tallest = h

    return tallest_object

  def Play_string(self, string, lang='en'):
    """Convert a string to speech audio and play it

    Args:
        string (string): The string to convert
        lang (str, optional): Target language. Defaults to 'en'.
    """    
    # Load audio from server
    tts = gTTS(text=string, lang=lang)
    
    # Convert to I/O object
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    # Play speech from temporary file
    speech = AudioSegment.from_file(fp, format="mp3")
    play(speech)

  def main(self, memory, objects):   
    """
    1. Search for LEGO Figures.
        Find Yellow and the color underneath
    2. Find the destination
        Find the color and check if not yellow

    Args:
        memory (Memory): Memory of the robot
        objects (list): Identified objects
    """    
    # Stop motors and await new orders
    self.stop()

    # If we need to drive a bit back, do that first
    if memory.drive_back:
      self.go_backward(self.speed)
      memory.drive_back_counter -= 1
      if memory.drive_back_counter <= 0:
        memory.drive_back = False
      
      return memory

    # FREE STATE: We are going to interpret the LEGO figure
    if memory.state == "Free":
      
      # Timer exceeding limit; no lego figure found
      if time.time() - memory.start_time > 10.0:
        message = 'No more customers? I will get some coffee.'
        self.Play_string(message, 'en')
        exit(0)

      # If we cannot find objects, return memory
      if not objects:
        print('No objects found!')
        self.stop()
        return memory

      # Identify all yellow objects (lego heads) and determine where the head is
      else:
        yellow_objects = [x for x in objects if x.colour == 'yellow']
        if yellow_objects:
          lego_head = self.find_largest(yellow_objects, 'yellow')
          # Find the location of the neck of the figure, where it should meet a shirt
          lego_neck = lego_head.location[1] + lego_head.size[1]
        else:
          print('No LEGO figure found')
          return memory

        # Now check if there is an object under the lego head, which should be a shirt
        for object in objects:
          if (object.location[1] in range(lego_neck - 20, lego_neck + 20)) and object.colour != 'yellow':
            print('LEGO FIGURE with shirt colour {0}'.format(object.colour))

            # Set goal colour and vacancy status
            memory.goal_colour = object.colour
            message = 'Hello Mister {0}, I am driving you to the {0} building!'.format(memory.goal_colour)
            self.Play_string(message)
            
            memory.state = "driving_to_goal"
            return memory

        # If nothing is found, just return the memory
        return memory
    
    # DRIVING TO GOAL STATE: We have a customer, let's bring him to his building
    elif memory.state == "driving_to_goal":
      print('Our destination is the {0} building.'.format(memory.goal_colour))
      destination_objects = [x for x in objects if x.colour == memory.goal_colour]

      # The goal cannot be found
      if not destination_objects:
        print('I cannot see the building!')

        # Turn left if we have never seen our target
        if not memory.target_spotted:
          print('I lost the building for too long... Looking for the building again!')
          self.go_left(self.speed)

        # Else, if time not exceeded, Drive on memory
        elif memory.spot_counter > 0:
          memory.spot_counter -= 1 # reduce timer

          print('Driving on memory! Spot Counter: ', memory.spot_counter)

          # Back to the base if we found the object
          if self.drive_toward_object(memory.last_object):
            print('Reached the goal! Back to the base!')
            message = 'Goodbye Mister {0}. I am returning to base.'.format(memory.goal_colour)
            self.Play_string(message)

            memory.state = "back_to_base"
            memory.target_spotted = False
            memory.spot_counter = 20
            memory.drive_back = True
            memory.drive_back_counter = self.drive_back_counter_default
        
        # Start looking for the target if we looked too long
        else:
          memory.spot_counter = 20
          memory.target_spotted = False
        
      # Target in sight, drive towards it
      else:
        memory.target_spotted = True
        memory.spot_counter = 20
        self.stop()

        # Find the tallest object (this is most probably the building)
        tallest_building = self.Find_tallest(destination_objects)
        memory.last_object = tallest_building

        # Back to the base if we found the object
        if self.drive_toward_object(tallest_building):
          print('Reached the goal! Back to the base!')
          message = 'Goodbye Mister {0}. I am returning to base.'.format(memory.goal_colour)
          self.Play_string(message)
          memory.state = "back_to_base"
          memory.target_spotted = False
          memory.drive_back = True
          memory.drive_back_counter = self.drive_back_counter_default

    #BACK TO BASE STATE: We have reached the goal, so we can return to the base
    elif memory.state == "back_to_base":
      destination_objects = [x for x in objects if x.colour == memory.base_colour]
      print('I am returning to base')

      # The goal cannot be found
      if not destination_objects:

        # Turn left if we have never seen our target
        if not memory.target_spotted:
          self.go_left(self.speed)

        # Drive on memory
        elif memory.spot_counter > 0:
          memory.spot_counter -= 1

          #Look for new lego figure if we found the base
          if self.drive_toward_object(memory.last_object):
            print('Back at the base!')
            message = 'We have arrived at the base! Looking for new customers!'.format(memory.goal_colour)
            self.Play_string(message)
            memory.state = "Free"
            memory.start_time = time.time()
            memory.target_spotted = False
            memory.spot_counter = 20
            memory.drive_back = True
            memory.drive_back_counter = self.drive_back_counter_default

        # Start looking for the target if we looked too long
        else:
          memory.spot_counter = 20
          memory.target_spotted = False
      
      # Target in sight, drive towards it
      else:
        base_building = self.Find_tallest(destination_objects)

        #Look for new lego figure if we found the base
        if self.drive_toward_object(base_building):
          message = 'We have arrived at the base! Looking for new customers!'.format(memory.goal_colour)
          self.Play_string(message)
          memory.state = "Free"
          memory.start_time = time.time()
          memory.target_spotted = False
          memory.drive_back = True
          memory.drive_back_counter = self.drive_back_counter_default

    else:
      print("This should not happen", memory.state)
    
    return memory

  def drive_toward_object(self, object):
    """ Make the robot drive towards an identified object

    Args:
        object (Object): identified object. Target location

    Returns:
        bool: If the object is still in sight
    """    
    x, y = object.location
    w, h = object.size
    
    object_centre = x + (w / 2)

    print('Object location: {0}. Left: {1}, Right: {2}'.format(object_centre, self.boundary_left, self.boundary_right))
    print('Object dimensions: (x,y): ({0},{1}), (w,h): ({2},{3})'.format(x, y, w, h))

    if h > 160 and w > 85: # If it reaches top of screen, it is probably very close
      print("destination reached")
      return True

    if object_centre > self.boundary_right: # Try to centre the object
      print("drive right")
      self.go_right(self.speed)

    elif object_centre < self.boundary_left: # Try to center other boundary
      print("drive left")
      self.go_left(self.speed)

    else:
      print("drive forward")
      self.go_forward(self.speed)

    return False
