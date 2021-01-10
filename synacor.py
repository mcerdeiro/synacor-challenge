#!/usr/bin/python3
from sys import stdin
from collections import deque
from getkey import getkey
from datetime import datetime
from mycpu import mycpu
from mycpu import memorydumping
from mycpu import debug
from mycpu import arrows


cpu = mycpu.MyCpu()
memdump = memorydumping.MemoryDummping(cpu)
dbg = debug.Debug(cpu, memdump)
arrows = arrows.Arrows(cpu)


f = open("challenge.bin", "rb")
cpu.loadBinary(f)
cpu.run()

