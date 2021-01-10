from collections import deque
from mycpu import instructions as inst

class MyCpu():
  debug = False
  callbacks = dict()
  reg: dict()
  stack: deque()
  mem: []
  inst: inst.Instructions
  breakpoints: []
  regbp: []

  def __init__(self):
    self.breakpoints = []
    self.regbp = []
    self.inst = inst.Instructions(self)
    self.mem = dict()
    self.reg = {"ip": 0}
    for i in range(8):
      self.reg[i] = 0
    self.stack = deque()

  def addCallback(self, function, callback):
    if function not in self.callbacks.keys():
      self.callbacks[function] = []
    self.callbacks[function].append(callback)

  def loadBinary(self, f):
    self.stack = deque()
    self.reg = {"ip": 0}
    for i in range(8):
      self.reg[i] = 0
    count = 0
    try:
      low = f.read(1)
      high = f.read(1)
      while (low != b"") & (high != b""):
          self.mem[count] = ord(high) * 256 + ord(low)
          count += 1
          low = f.read(1)
          high = f.read(1)

    finally:
      f.close()

  def loadCpuState(self, reg, stack, mem):
    self.reg = reg
    self.stack = stack
    self.mem = mem
  
  def getCpuState(self):
    return self.reg, self.stack, self.mem

  def run(self):
    while True:
      self._execute()
      self.reg["ip"] += 1

  def _execute(self):
    if self.reg["ip"] in self.breakpoints:
      self.debug = True
      print("**** Breakpoint ****")
    if self.debug:
      if "debug" in self.callbacks.keys():
        self.callbacks["debug"][0]()
    cmd = self.mem[self.reg["ip"]]
    instlist = {
      0: self.inst._halt,
      1: self.inst._set,
      2: self.inst._push,
      3: self.inst._pop,
      4: self.inst._eq,
      5: self.inst._gt,
      6: self.inst._jmp,
      7: self.inst._jt,
      8: self.inst._jf,
      9: self.inst._add,
      10: self.inst._mult,
      11: self.inst._mod,
      12: self.inst._and,
      13: self.inst._or,
      14: self.inst._not,
      15: self.inst._rmem,
      16: self.inst._wmem,
      17: self.inst._call,
      18: self.inst._ret,
      19: self.inst._stdout,
      20: self.inst._stdin,
      21: self.inst._nop
    }
    if cmd not in instlist.keys():
      print("Trying to execute unkonw instruction:", str(cmd))
      assert(0)
    else:
      instlist[cmd]()

  def _getValPar(self, n: int):
      val = self.mem[self.reg["ip"]+1+n]
      if val <= 32767:
        return val
      elif 32767 < val <= 32775:
        if (val-32768) in self.regbp:
          print(f"Breakpont read r{val-32768} at {self.reg['ip']}")
          self.debug = True
        return self.reg[val-32768]
      assert(0)
      return None

  def _setRegister(self, n, val):
      r = self.mem[self.reg["ip"]+n+1]
      assert(r >= 32768)
      if (r-32768) in self.regbp:
          print(f"Breakpont write r{r-32768} at {self.reg['ip']}")
          self.debug = True
      self.reg[r-32768] = val
