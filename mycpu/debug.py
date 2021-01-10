from mycpu import mycpu
from mycpu import memorydumping
from collections import deque

class Debug():
  cpu: mycpu.MyCpu
  memdump: memorydumping.MemoryDummping
  debug = False
  tele = -1
  lastcmd = ""
  
  completestdouts = deque()
  currentstdout = ""
  vault: int
  waitinst = None

  def __init__(self, cpu, memdump):
    self.cpu = cpu
    self.cpu.addCallback("stdin", self.keycallback)
    self.cpu.addCallback("stdinhandler", self.getInputCallback)
    self.cpu.addCallback("stdout", self.outcallback)
    self.cpu.addCallback("debug", self.debugConsole)
    self.memdump = memdump
    self.lastcmd = ""
    self.vault = 0
    self.waitinst = None
    self.lookup = {
        0: { "n": "halt", "p": 0, "d": "" },
        1: { "n": "set", "p": 2, "d": "", "s": "p0 = p1" },
        2: { "n": "push", "p": 1, "d": "",},
        3: { "n": "pop", "p": 1, "d": "" },
        4: { "n": "eq", "p": 3, "d": "", "s": "p0 = (p1 == p2)"},
        5: { "n": "gt", "p": 3, "d": "", "s": "p0 = (p1 > p2)" },
        6: { "n": "jmp", "p": 1, "d": "" },
        7: { "n": "jt", "p": 2, "d": "jump if p0 not zero", "s": "if p0 != 0: jmp p1" },
        8: { "n": "jf", "p": 2, "d": "jump if p0 zero", "s": "if p0 == 0: jmp p1" },
        9: { "n": "add", "p": 3, "d": "", "s": "p0 = p1 + p2" },
        10: { "n": "mult", "p": 3, "d": "", "s": "p0 = p1 * p2" },
        11: { "n": "mod", "p": 3, "d": "", "s": "p0 = p1 % p2" },
        12: { "n": "and", "p": 3, "d": "", "s": "p0 = p1 & p2" },
        13: { "n": "or", "p": 3, "d": "", "s": "p0 = p1 | p2" },
        14: { "n": "not", "p": 2, "d": "", "s": "p0 = ~p1" },
        15: { "n": "rmem", "p": 2, "d": "" },
        16: { "n": "wmem", "p": 2, "d": "" },
        17: { "n": "call", "p": 1, "d": "" },
        18: { "n": "ret", "p": 0, "d": "" },
        19: { "n": "out", "p": 1, "d": "" },
        20: { "n": "in", "p": 1, "d": "" },
        21: { "n": "nop", "p": 0, "d": "" },
      }

  def outcallback(self, out):
    if out == 10:
      self.completestdouts.append(self.currentstdout)
      if self.tele > 0:
        if "1 billion years." in self.currentstdout:
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
      self.cpu.debug = True
      return "use teleporter"
    if self.vault == 1:
      self.cpu.debug = True
      return "east"
    return None

  def _rb(self, opt = ""):
    r = int(opt.split()[0])
    self.cpu.regbp.append(r)

  def _changevar(self, opt= ""):
    reg = opt.split()[0]
    val = int(opt.split()[1])
    if reg == "ip":
      self.cpu.reg["ip"] = val
    elif "r" in reg:
      reg = int(reg[1])
      self.cpu.reg[reg] = val
    else:
      print("unkown register", reg)

  def _b(self, opt = ""):
    ip = int(opt.split()[0])
    self.cpu.breakpoints.append(ip)

  def _p(self, opt = ""):
    tmp = ""
    for k,v in self.cpu.reg.items():
      tmp += str(k) + ":" + str(v) + " "
    print("Reg:",tmp, "Stack len:", len(self.cpu.stack))

  def _dissas(self, opt):
    count = 1
    if opt != "":
      count = int(opt.split()[0])
    offset = 0
    while count > 0:
      count -= 1
      ip = self.cpu.reg["ip"] + offset
      cmd = self.cpu.mem[ip]

      if cmd not in self.lookup.keys(): 
        print("Command not found in dissasembly lookuptable:", cmd)
        print("Aborting..")
        return
      params = self.lookup[cmd]['p']
      reg = ""
      s = ""
      so = ""
      if "s" in self.lookup[cmd].keys():
        s = self.lookup[cmd]["s"]
        so = s
      for idx in range(params):
        tmp = self.cpu.mem[ip+1+idx]
        if tmp <= 32767:
          reg += f"{tmp} "
          s = s.replace("p"+str(idx), str(tmp))
        else:
          reg += f"r{tmp-32768}({self.cpu.reg[tmp-32768]}) "
          s = s.replace("p"+str(idx), "r" + str(tmp-32768) + f"({self.cpu.reg[tmp-32768]})")

      if s != "":
        tmp = f"ip {ip}: {self.lookup[cmd]['n']} " + s + f"   /   ({so})   /   " + self.lookup[cmd]["d"]
      else:
        tmp = f"ip {ip}: {self.lookup[cmd]['n']} " + reg + "    /    " + self.lookup[cmd]["d"]
      print(tmp)
      offset += 1 + params

  def _stacktrace(self, opt):
    print("Stack:", self.cpu.stack)

  def waitCmd(self, opt):
    self.waitinst = opt
    print("Waiting for:", self.waitinst)

  def waitInst(self):
    if self.waitinst == None:
      return False
    return True

  def debugConsole(self):
    self._p()
    self._dissas("1")
    if self.waitInst():
      return
    contdebug = True
    while contdebug:
      val = input("> ")
      if val == "":
        val = self.lastcmd
      else:
        self.lastcmd = val

      opt = {
        "p": self._p,
        "d": self._dissas,
        "b": self._b,
        "rb": self._rb,
        "st": self._stacktrace,
        "set": self._changevar,
        "w": self.waitCmd
      }
      dcmd = val.split()[0]
      drest = ""
      if len(val) > len(dcmd) + 1:
        drest = val.replace(dcmd + " ", "")
      if dcmd in opt.keys():
        opt[dcmd](drest)
      elif val == "n":
        contdebug = False
      elif val == "cont":
        contdebug = False
        self.cpu.debug = False
      elif val == "tele off":
        self.tele = 0
        self.cpu.debug = False
      else:
        print("Unkown command, try help")


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
          if cmd == "console":
            self.cpu.debug = True
          if cmd == "vault":
            self.vault = 1
          if cmd == "cont":
            cont = False
          if cmd == "p":
            self._p()
          if cmd == "tele":
            self.tele = 1
