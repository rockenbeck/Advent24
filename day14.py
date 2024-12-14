import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input14 import *

test14="""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

def day14a(s,dX,dY):
    robots = []

    for line in s.split("\n"):
        m = re.match(r"p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)", line)
        robots.append(tuple(map(int,m.groups())))

    quads=[0] * 4
    cSec = 100
    for pX,pY,vX,vY in robots:
        endX,endY = (pX + vX * cSec) % dX, (pY + vY * cSec) % dY

        if endX == dX // 2 or endY == dY // 2:
            continue

        iQuad = 0
        if endY > dY // 2:
            iQuad += 2
        if endX > dX // 2:
            iQuad += 1

        quads[iQuad] += 1

    print(f"safety factor = {math.prod(quads)}")

# day14a(test14,11,7)
# day14a(input14,101,103)

def day14b(s,dX,dY):
    robots = []

    for line in s.split("\n"):
        m = re.match(r"p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)", line)
        robots.append(tuple(map(int,m.groups())))

    # 577 has almost a picture in X
    # 678 has another
    # 31 lots of blanks at bottom
    # 134 again
    # use Chinese Remainder Theorem to solve
    #  n = 72 % 101
    #  n = 31 % 103
    # Found a solver on the web: https://www.dcode.fr/chinese-remainder
    #  n = 7344

    r = 1 # reduction factor to see all on terminal output

    # for cSec in range(0,3000):            # initial search
    # for cSec in range(577,dX * dY,dX):    # note some order in this one
    # for cSec in range(31,100000,dY):      # note different order in this one
    for cSec in range(7344,7345):           # CRT result
        mp = set()
        for pX,pY,vX,vY in robots:
            mp.add((((pX + vX * cSec) % dX) // r, ((pY + vY * cSec) % dY) // r))
        sOut = ""
        for y in range(dY//r):
            for x in range(dX//r):
                sOut += '*' if (x,y) in mp else '.'
            sOut += "\n"
        
        print(f"After {cSec} seconds:\n{sOut}\n\n")
        input("Press Enter to continue...")

day14b(input14,101,103)

