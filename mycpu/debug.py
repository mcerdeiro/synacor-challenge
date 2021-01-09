from mycpu import mycpu
from mycpu import memorydumping
from collections import deque

class Debug():
  cpu: mycpu.MyCpu
  memdump: memorydumping.MemoryDummping
  debug = False
  tele = -1
  
  completestdouts = deque()
  currentstdout = ""

  def __init__(self, cpu, memdump):
    self.cpu = cpu
    self.cpu.addCallback("stdin", self.keycallback)
    self.cpu.addCallback("stdinhandler", self.getInputCallback)
    self.cpu.addCallback("stdout", self.outcallback)
    self.cpu.addCallback("debug", self.debugConsole)
    self.memdump = memdump

  def outcallback(self, out):
    if out == 10:
      self.completestdouts.append(self.currentstdout)
      if self.tele > 0:
        if "1 billion years." in self.currentstdout:
          self.memdump._load()
          self.cpu.reg["ip"] -= 1
          self.cpu.debug = True
      self.currentstdout = ""
    else:
      self.currentstdout = self.currentstdout + chr(out)
    if len(self.completestdouts) > 100:
      self.completestdouts.popleft()

  def getInputCallback(self):
    if self.tele > 0:
      print("Tele with", self.tele)
      self.cpu.reg[7] = self.tele
      self.tele += 1
      return "use teleporter"
    return None

  def debugConsole(self):
    pass

  def keycallback(self, key):
    if key == b'\x1bOP': #F1
      if self.debug:
        self.debug = False
      else:
        self.debug = True
      print("Debug:", self.debug)

    if self.debug:
      #print("Key", key)
      if key == b'\x1bOQ':
        cont = True
        while cont:
          cmd = input("Debug command: ")
          if cmd == "cont":
            cont = False
          if cmd == "p":
            tmp = ""
            for k,v in self.cpu.reg.items():
              tmp += str(k) + ":" + str(v) + " "
            print("Reg:",tmp)
          if cmd == "tele":
            self.tele = 1
