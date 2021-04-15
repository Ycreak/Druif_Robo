# class Building:
#   def __init__(self):

#     self.location:
#     self.

class Processor:
  def __init__(self):

    self.free = True

  def Check_largest(self, object, biggest):
    w,h = object.size
    # Assignment
    biggest_object = object


    if (w+h) > biggest:
      biggest_object = object
      biggest = w+h

    return biggest, biggest_object


  def main(self, objects):   
    """
    1. Search for LEGO Figures.
        Find Yellow and the color underneath
    2. Find the destination
        Find the color and check if not yellow

    Args:
        objects ([type]): [description]
    """    
    
    if self.free: 
      # Find a LEGO figure to pickup
 
      biggest = 0
      biggest_yellow = 0
      biggest_red = 0

      # Try, because we cannot always find an object (maybe check if objects is filled)
      if objects:
          for object in objects:
              
              if object.colour == 'yellow':
                biggest_yellow, biggest_yellow_object = self.Check_largest(object, biggest_yellow)

              elif object.colour == 'red':
                biggest_red, biggest_red_object = self.Check_largest(object, biggest_red)

          # Find shirt
          head_lower = biggest_yellow_object.location[1] + biggest_yellow_object.size[1]
          
          try:
            if biggest_red_object:
              shirt_top = biggest_red_object.location[1]
              if(shirt_top in range(head_lower - 20, head_lower + 20)):
                print('LEGO FIGURE')

          except:
            pass

            # Yes? Drive towards it and register its colour.

            # No? Keep driving around until you find one.
          
          # print("Location: {0}, Size: {1}, Colour: {2}".format(object.location, object.size, object.colour))
          
          # self.drive_toward_object(biggest_object)
      
      else:
          print('No objects')

    else:
      # We are occupied, find the destination
      pass

  def drive_toward_object(self, object):
    x, y = object.location

    if y < 100: # If it reaches top of screen, it is probably very close
      print("destination reached")
    elif x > 270: # Try to centre the object
      print("drive left") # i cant think mirrored
    elif x < 210:
      print("drive right")
    else:
      print("drive forward")

    print(x,y)