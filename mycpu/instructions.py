from getkey import getkey
from collections import deque

class Instructions():
  class StdinHandler():
    command: deque()

    def __init__(self, inst):
      self.inst = inst
      self.command = deque()

    def _getCommand(self):
      read = None
      if len(self.command) == 0:
        if "stdinhandler" in self.inst.cpu.callbacks.keys():
          for cb in self.inst.cpu.callbacks["stdinhandler"]:
            read = cb()
            if read != None:
              self.command = deque([x for x in read]+[chr(10)])
      if len(self.command) > 0:
        read = self.command.popleft()

      return read

    def get(self):
      read = self._getCommand()
      if read == None:
        read = getkey()
      
      if len(read) != 1:
        utf = read.encode("utf")
        if "stdin" in self.inst.cpu.callbacks.keys():
          for cb in self.inst.cpu.callbacks["stdin"]:
            cb(utf)
        read = chr(10)
        
      return read

  def __init__(self, cpu):
    self.cpu = cpu
    self.stdinhandler = self.StdinHandler(self)

  # halt: 0
  # stop execution and terminate the program
  def _halt(self):
    if self.cpu.debug:
      print("halt: 0 -stop execution and terminate the program")
    print("halt")

  # set: 1 a b
  # set register <a> to the value of <b>
  def _set(self):
    self.cpu._setRegister(0, self.cpu._getValPar(1))
    self.cpu.reg["ip"] += 2

  # push: 2 a
  # push <a> onto the stack
  def _push(self):
    p1 = self.cpu._getValPar(0)
    self.cpu.stack.insert(0, p1)
    self.cpu.reg["ip"] += 1
  
  # pop: 3 a
  # remove the top element from the stack and write it into <a>; empty stack = error
  def _pop(self):
    assert(len(self.cpu.stack) > 0)
    self.cpu._setRegister(0, self.cpu.stack.popleft())
    self.cpu.reg["ip"] += 1

  # eq: 4 a b c
  # set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
  def _eq(self):
    self.cpu._setRegister(0, self.cpu._getValPar(1) == self.cpu._getValPar(2))
    self.cpu.reg["ip"] += 3

  # gt: 5 a b c
  # set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
  def _gt(self):
    self.cpu._setRegister(0, self.cpu._getValPar(1) > self.cpu._getValPar(2))
    self.cpu.reg["ip"] += 3
      
  # jmp: 6 a
  # jump to <a>
  def _jmp(self):
    val = self.cpu._getValPar(0)
    self.cpu.reg["ip"] = val - 1

  # jt: 7 a b
  # if <a> is nonzero, jump to <b>
  def _jt(self):
    p1 = self.cpu._getValPar(0)
    p2 = self.cpu._getValPar(1)
    if p1 != 0:
        self.cpu.reg["ip"] = p2 - 1
    else:
        self.cpu.reg["ip"] += 2

  # jf: 8 a b
  # if <a> is zero, jump to <b>
  def _jf(self):
    p1 = self.cpu._getValPar(0)
    p2 = self.cpu._getValPar(1)
    if p1 == 0:
        self.cpu.reg["ip"] = p2 - 1
    else:
        self.cpu.reg["ip"] += 2

  # add: 9 a b c
  # assign into <a> the sum of <b> and <c> (modulo 32768)  
  def _add(self):
    self.cpu._setRegister(0, (self.cpu._getValPar(1) + self.cpu._getValPar(2)) % 32768)
    self.cpu.reg["ip"] += 3

  # mult: 10 a b c
  # store into <a> the product of <b> and <c> (modulo 32768)
  def _mult(self):
    self.cpu._setRegister(0, (self.cpu._getValPar(1) * self.cpu._getValPar(2)) % 32768)
    self.cpu.reg["ip"] += 3

  # mod: 11 a b c
  # store into <a> the remainder of <b> divided by <c>
  def _mod(self):
    self.cpu._setRegister(0, (self.cpu._getValPar(1) % self.cpu._getValPar(2)) % 32768)
    self.cpu.reg["ip"] += 3
  
  # and: 12 a b c
  # stores into <a> the bitwise and of <b> and <c>
  def _and(self):
    self.cpu._setRegister(0, self.cpu._getValPar(1) & self.cpu._getValPar(2))
    self.cpu.reg["ip"] += 3
  
  # or: 13 a b c
  # stores into <a> the bitwise or of <b> and <c>
  def _or(self):
    self.cpu._setRegister(0, self.cpu._getValPar(1) | self.cpu._getValPar(2))
    self.cpu.reg["ip"] += 3

  # not: 14 a b
  # stores 15-bit bitwise inverse of <b> in <a>
  def _not(self):
    self.cpu._setRegister(0, (~self.cpu._getValPar(1)) & 32767)
    self.cpu.reg["ip"] += 2
  
  # rmem: 15 a b
  # read memory at address <b> and write it to <a>
  def _rmem(self):
    p1 = self.cpu._getValPar(1)
    self.cpu._setRegister(0, self.cpu.mem[p1])
    self.cpu.reg["ip"] += 2

  # wmem: 16 a b
  # write the value from <b> into memory at address <a>
  def _wmem(self):
    p0 = self.cpu._getValPar(0)
    p1 = self.cpu._getValPar(1)
    self.cpu.mem[p0] = p1
    self.cpu.reg["ip"] += 2

  # call: 17 a
  # write the address of the next instruction to the stack and jump to <a>
  def _call(self):
    self.cpu.stack.insert(0, self.cpu.reg["ip"]+2)
    p1 = self.cpu._getValPar(0)
    self.cpu.reg["ip"] = p1 - 1
  
  # ret: 18
  # remove the top element from the stack and jump to it; empty stack = halt
  def _ret(self):
    assert(len(self.cpu.stack) > 0)
    p = self.cpu.stack.popleft()
    self.cpu.reg["ip"] = p - 1

  # out: 19 a
  # write the character represented by ascii code <a> to the terminal
  def _stdout(self):
      #if debug:
      #    print("out: 19 a -write the character represented by ascii code <a> to the terminal")
      val = self.cpu._getValPar(0)
      print(chr(val), end="")
      self.cpu.reg["ip"] += 1
      if "stdout" in self.cpu.callbacks.keys():
        for cb in self.cpu.callbacks["stdout"]:
          cb(val)

      # lastprints.append(chr(val))
      # if len(lastprints) > 50:
      #     lastprints.popleft()
      # if ("".join(list(lastprints)[-len("exits:")-1:-1])=="exits:"):
      #     options = []
      #     creatingoptions = True

      # if ("".join(list(lastprints)[-len("What do you do?")-1:-1])=="What do you do?"):
      #         print("Reg 8th:", reg[7])
      #         reg[7] = 1
      # if creatingoptions == True:
      #     if ("".join(list(lastprints)[-len("What do you do?")-1:-1])=="What do you do?"):
      #         creatingoptions = False
      #         print("Options", options)
      #         print("Reg 8th:", reg[7])
      #     if ("".join(list(lastprints)[-len("- ")-1:-1])=="- "):
      #         print(f"[{len(options)}] ", end="")
      #         option = ""
      #     option = option + chr(val)
      #     if val == 10:
      #         if len(option) > 2:
      #             options.append(option[0:-1])
      #             option = ""
      #         else:
      #             #creatingoptions = False
      #             pass

  # in: 20 a
  # read a character from the terminal and write its ascii code to <a>; it can be assumed that once input starts, it will continue until a newline is encountered; this means that you can safely read whole lines from the keyboard and trust that they will be fully read
  def _stdin(self):
    read = self.stdinhandler.get()
    self.cpu._setRegister(0, ord(read))
    self.cpu.reg["ip"] += 1

    
        
        # if len(read) == 1:
        #     if read in ["0", "1", "2", "3", "4", "5", "6"] and ord(read)-ord("0") < len(options):
        #         #print(f"Selection: \"{options[ord(read)-ord('0')]}\"")
        #         going = True
        #         go = deque([x for x in options[ord(read)-ord("0")]])
        #         print(f"Going to: \"{''.join(go)}\" - {len(go)}")
        #         go.append(chr(10))
        #     else:
        #         #print("Writing", read, ord(read))
        #         setRegister(0, ord(read))
        # else:
        #     utf = read.encode("utf")
        #     if utf == b'\x1b[A':
        #         go = deque([x for x in "go north" + chr(10)])
        #         print("".join(go))
        #         going = True
        #     elif utf == b'\x1b[B':
        #         go = deque([x for x in "go south" + chr(10)])
        #         print("".join(go))
        #         going = True
        #     elif utf == b'\x1b[C':
        #         go = deque([x for x in "go east" + chr(10)])
        #         print("".join(go))
        #         going = True
        #     elif utf == b'\x1b[D':
        #         go = deque([x for x in "go west" + chr(10)])
        #         print("".join(go))
        #         going = True
        #     elif utf == b'\x1b[24~':
        #         #now = datetime.now()
        #         #filename = now.strftime("%Y_%m_%d_%H:%M:%S.bin")
        #         filename = "stored.bin"
        #         print("Saving to " + filename + "...")
        #         f = open(filename, "wb")
        #         data = {"reg": reg, "stack": stack, "mem": mem}
        #         pickle.dump(data, f)
        #         f.close()
        #     elif utf == b'\x1b[20~':
        #         return utf
        #     else:
        #         print("Unkonw command", utf)
        #     setRegister(0, 10)
      
      
  # noop: 21
  # no operation
  def _nop(self):
    pass