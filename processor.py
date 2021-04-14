# class Building:
#   def __init__(self):

#     self.location:
#     self.

class Processor:
  def __init__(self):

    self.free = True


  def main(self, objects):   
    
    
    if self.free: 
      # Find a LEGO figure to pickup
 
      biggest = 0

      try:
          for object in objects:
              w,h = object.size
              if (w+h) > biggest:
                biggest_object = object
                biggest = w+h

              # Is one of the objects a LEGO figure?

                # Yes? Drive towards it and register its colour.

                # No? Keep driving around until you find one.
              
              # print("Location: {0}, Size: {1}, Colour: {2}".format(object.location, object.size, object.colour))
          
          self.drive_toward_object(biggest_object)
      
      except:
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