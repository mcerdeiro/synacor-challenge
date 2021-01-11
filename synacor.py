#!/usr/bin/python3
from sys import stdin
from collections import deque
from getkey import getkey
from datetime import datetime
from mycpu import mycpu
from mycpu import memorydumping
from mycpu import debug
from mycpu import arrows

print("""
F1  Starts the debugger console
F9  Loads the memory, stack and register state from stored.bin
F12 Stores the current state of memory, stack and register into stored.bin
""")
cpu = mycpu.MyCpu()
memdump = memorydumping.MemoryDummping(cpu)
dbg = debug.Debug(cpu, memdump)
arrows = arrows.Arrows(cpu)


f = open("challenge.bin", "rb")
cpu.loadBinary(f)
cpu.run()

