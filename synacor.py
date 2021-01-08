#!/usr/bin/python3
from sys import stdin
from collections import deque
from getkey import getkey
from datetime import datetime
import pickle

count = 0
f = open("challenge.bin", "rb")
debug = True

mem = dict()
reg = {"ip": 0}
for i in range(8):
    reg[i] = 0
stack = deque()

try:
    low = f.read(1)
    high = f.read(1)
    while (low != b"") & (high != b""):
        mem[count] = ord(high) * 256 + ord(low)
        #print("count", count, mem, ord(high), ord(low))
        count += 1
        low = f.read(1)
        high = f.read(1)
        
finally:
    f.close()


def getValPar(n: int):
    val = mem[reg["ip"]+1+n]
    if val <= 32767:
        return val
    elif 32767 < val <= 32775:
        return reg[val-32768]

    assert(0)

    return None

def setRegister(n, val):
    r = mem[reg["ip"]+n+1]
    assert(r >= 32768)
    reg[r-32768] = val


def command():
    global reg, stack, mem
    go = deque()
    going = False

    lastprints = deque()
    options = []
    option = ""
    creatingoptions = False

    while True:
        cmd = mem[reg["ip"]]
        if cmd == 0:
            if debug:
                print("halt: 0 -stop execution and terminate the program")
            print("halt")
            exit()
        elif cmd == 1:
            setRegister(0, getValPar(1))
            reg["ip"] += 2
        elif cmd == 2:
            p1 = getValPar(0)
            stack.insert(0, p1)
            reg["ip"] += 1
        elif cmd == 3:
            assert(len(stack) > 0)
            setRegister(0, stack.popleft())
            reg["ip"] += 1
        elif cmd == 4:
            setRegister(0, getValPar(1) == getValPar(2))
            reg["ip"] += 3
        elif cmd == 5:
            setRegister(0, getValPar(1) > getValPar(2))
            reg["ip"] += 3
        elif cmd == 6:
            val = getValPar(0)
            # if debug:
            #     print(f"jmp: 6 a -jump to <{val}>")
            reg["ip"] = val - 1
        elif cmd == 7:
            # if debug:
            #     print("jt: 7 a b -if <a> is nonzero, jump to <b>")
            p1 = getValPar(0)
            p2 = getValPar(1)
            if p1 != 0:
                reg["ip"] = p2 - 1
            else:
                reg["ip"] += 2
        elif cmd == 8:
            p1 = getValPar(0)
            p2 = getValPar(1)
            if p1 == 0:
                reg["ip"] = p2 - 1
            else:
                reg["ip"] += 2
        elif cmd == 9:
            setRegister(0, (getValPar(1) + getValPar(2)) % 32768)
            reg["ip"] += 3
        elif cmd == 10:
            setRegister(0, (getValPar(1) * getValPar(2)) % 32768)
            reg["ip"] += 3
        elif cmd == 11:
            setRegister(0, (getValPar(1) % getValPar(2)) % 32768)
            reg["ip"] += 3
        elif cmd == 12:
            setRegister(0, getValPar(1) & getValPar(2))
            reg["ip"] += 3
        elif cmd == 13:
            setRegister(0, getValPar(1) | getValPar(2))
            reg["ip"] += 3
        elif cmd == 14:
            setRegister(0, (~getValPar(1)) & 32767)
            reg["ip"] += 2
        elif cmd == 15:
            p1 = getValPar(1)
            setRegister(0, mem[p1])
            reg["ip"] += 2
        elif cmd == 16:
            p0 = getValPar(0)
            p1 = getValPar(1)
            mem[p0] = p1
            reg["ip"] += 2
        elif cmd == 17:
            stack.insert(0, reg["ip"]+2)
            p1 = getValPar(0)
            reg["ip"] = p1 - 1
        elif cmd == 18:
            assert(len(stack) > 0)
            p = stack.popleft()
            reg["ip"] = p - 1
        elif cmd == 19:
            #if debug:
            #    print("out: 19 a -write the character represented by ascii code <a> to the terminal")
            val = getValPar(0)
            lastprints.append(chr(val))
            if len(lastprints) > 50:
                lastprints.popleft()
            if ("".join(list(lastprints)[-len("exits:")-1:-1])=="exits:"):
                options = []
                creatingoptions = True

            if creatingoptions == True:
                if ("".join(list(lastprints)[-len("What do you do?")-1:-1])=="What do you do?"):
                    creatingoptions = False
                    print("Options", options)
                if ("".join(list(lastprints)[-len("- ")-1:-1])=="- "):
                    print(f"[{len(options)}] ", end="")
                    option = ""
                option = option + chr(val)
                if val == 10:
                    if len(option) > 2:
                        options.append(option[0:-1])
                        option = ""
                    else:
                        #creatingoptions = False
                        pass


            print(chr(val), end="")

            reg["ip"] += 1
        elif cmd == 20:
            #if debug:
                #print("in: 20 a -read a character from the terminal and write its ascii code to <a>; it can be assumed that once input starts, it will continue until a newline is encountered; this means that you can safely read whole lines from the keyboard and trust that they will be fully read")
            if going:
                read = go.popleft()
                #print("Writing", read, ord(read))
                if len(go) == 0:
                    going = False
                setRegister(0, ord(read))
            else:
                read = getkey()
                
                if len(read) == 1:
                    if read in ["0", "1", "2", "3", "4", "5", "6"] and ord(read)-ord("0") < len(options):
                        #print(f"Selection: \"{options[ord(read)-ord('0')]}\"")
                        going = True
                        go = deque([x for x in options[ord(read)-ord("0")]])
                        print(f"Going to: \"{''.join(go)}\" - {len(go)}")
                        go.append(chr(10))
                    else:
                        #print("Writing", read, ord(read))
                        setRegister(0, ord(read))
                else:
                    utf = read.encode("utf")
                    if utf == b'\x1b[A':
                        go = deque([x for x in "go north" + chr(10)])
                        print("".join(go))
                        going = True
                    elif utf == b'\x1b[B':
                        go = deque([x for x in "go south" + chr(10)])
                        print("".join(go))
                        going = True
                    elif utf == b'\x1b[C':
                        go = deque([x for x in "go east" + chr(10)])
                        print("".join(go))
                        going = True
                    elif utf == b'\x1b[D':
                        go = deque([x for x in "go west" + chr(10)])
                        print("".join(go))
                        going = True
                    elif utf == b'\x1b[24~':
                        #now = datetime.now()
                        #filename = now.strftime("%Y_%m_%d_%H:%M:%S.bin")
                        filename = "stored.bin"
                        print("Saving to " + filename + "...")
                        f = open(filename, "wb")
                        data = {"reg": reg, "stack": stack, "mem": mem}
                        pickle.dump(data, f)
                        f.close()
                    elif utf == b'\x1b[20~':
                        filename = "stored.bin"
                        print("Loading " + filename)
                        f = open(filename, "rb")
                        data = pickle.load(f)
                        reg = data["reg"]
                        mem = data["mem"]
                        stack = data["stack"]
                        f.close()
                    else:
                        print("Unkonw command", utf)
                    setRegister(0, 10)
            reg["ip"] += 1
        elif cmd == 21:
            pass
            #if debug:
            #    print("noop: 21 -no operation")
        else:
            print("Unkonw inst found", cmd, "at", reg["ip"])
            exit()
        reg["ip"] += 1

command()

