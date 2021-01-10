from mycpu import mycpu
from mycpu import memorydumping

class Arrows:
  dir = None
  
  def __init__(self, cpu):
    self.cpu = cpu
    self.cpu.addCallback("stdin", self.keycallback)
    self.cpu.addCallback("stdinhandler", self.getInputCallback)
    self.dir = None

  def getInputCallback(self):
    ret = self.dir
    self.dir = None
    return ret
      

  def keycallback(self, key):
    #print("Key", key)
    #north
    if key == b'\x1b[A':
      self.dir ="north"
    #south
    elif key == b'\x1b[B':
      self.dir = "south"
      pass
    #east
    elif key == b'\x1b[C':
      self.dir = "east"
      pass
    #west
    elif key == b'\x1b[D':
      self.dir = "west"

