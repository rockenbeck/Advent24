import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input6 import *

test6="""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def parse(s):
    mp = {}

    yMax = 0
    for line in s.split('\n'):
        xMax = 0
        for ch in line:
            if ch in "^<>v":
                x,y,dir = xMax, yMax, ch
                ch = "."
            mp[(xMax,yMax)] = ch
            xMax += 1
        yMax += 1

    assert(x != None)

    return mp,xMax,yMax,x,y,dir
    
def day6a(s):
   
    mp,xMax,yMax,x,y,dir = parse(s)

    visits = set()

    while True:
        visits.add((x,y))

        if dir == "^":
            xNext,yNext,right = x,y-1,">"
        elif dir == "<":
            xNext,yNext,right = x-1,y,"^"
        elif dir == ">":
            xNext,yNext,right = x+1,y,"v"
        elif dir == "v":
            xNext,yNext,right = x,y+1,"<"
        else:
            assert(False)

        if (xNext,yNext) not in mp:
            break
        if mp[(xNext,yNext)] == "#":
            dir = right
        else:
            x,y = xNext,yNext

    print(len(visits))

    return visits


# day6a(test6)
# day6a(input6)


def day6b(s):
   
    mp,xMax,yMax,xStart,yStart,dirStart = parse(s)

    blockCount = 0

    # Brute force: try placing block everywhere possible,
    #  run from start to see whether it goes off edge before looping.
    # Interesting to consider what other algorithms might work here

    for yBlock in range(yMax):
        for xBlock in range(xMax):
            if xBlock == xStart and yBlock == yStart:
                continue
            if mp[(xBlock,yBlock)] == '#':
                continue
            assert(mp[(xBlock,yBlock)] == '.')

            # place temp obstruction
            mp[(xBlock,yBlock)] = '#'

            visits = set()
            x,y,dir = xStart,yStart,dirStart
            looped = False
            while True:
                if (x,y,dir) in visits:
                    looped = True
                    break
                visits.add((x,y,dir))

                if dir == "^":
                    xNext,yNext,right = x,y-1,">"
                elif dir == "<":
                    xNext,yNext,right = x-1,y,"^"
                elif dir == ">":
                    xNext,yNext,right = x+1,y,"v"
                elif dir == "v":
                    xNext,yNext,right = x,y+1,"<"
                else:
                    assert(False)

                if (xNext,yNext) not in mp:
                    break
                if mp[(xNext,yNext)] == "#":
                    dir = right
                else:
                    x,y = xNext,yNext

            # remove temp obstruction
            mp[(xBlock,yBlock)] = '.' 

            if looped:
                blockCount += 1

    print(blockCount)


def day6bv2(s):
   
    mp,xMax,yMax,xStart,yStart,dirStart = parse(s)

    # Pre-compute direction as a 2-D "vector"; not much faster

    if dirStart == "^":
        dXStart,dYStart = 0,-1
    elif dirStart == "<":
        dXStart,dYStart = -1,0
    elif dirStart == "v":
        dXStart,dYStart = 0,1
    elif dirStart == ">":
        dXStart,dYStart = 1,0
    else:
        assert(False)

    blockCount = 0

    for yBlock in range(yMax):
        for xBlock in range(xMax):
            if xBlock == xStart and yBlock == yStart:
                continue
            if mp[(xBlock,yBlock)] == '#':
                continue
            assert(mp[(xBlock,yBlock)] == '.')

            # place temp obstruction
            mp[(xBlock,yBlock)] = '#'

            visits = set()
            x,y,dX,dY = xStart,yStart,dXStart,dYStart
            looped = False
            while True:

                xNext,yNext = x+dX,y+dY
                if (xNext,yNext) not in mp:
                    break
                if mp[(xNext,yNext)] == "#":
                    if (x,y,dX,dY) in visits: # only need to check this occasionally; other algorithms possible, too
                        looped = True
                        break
                    visits.add((x,y,dX,dY))
                    dX,dY = -dY,dX
                else:
                    x,y = xNext,yNext

            # remove temp obstruction
            mp[(xBlock,yBlock)] = '.' 

            if looped:
                blockCount += 1

    print(blockCount)


def day6bv3(s):
   
    mp,xMax,yMax,xStart,yStart,dirStart = parse(s)

    if dirStart == "^":
        dXStart,dYStart = 0,-1
    elif dirStart == "<":
        dXStart,dYStart = -1,0
    elif dirStart == "v":
        dXStart,dYStart = 0,1
    elif dirStart == ">":
        dXStart,dYStart = 1,0
    else:
        assert(False)

    blockCount = 0

    # Only need to try placing new blocks where they will be encountered by guard,
    #  which is exactly what we determined in part A!

    visitsOrig = day6a(s)

    for (xBlock,yBlock) in visitsOrig:
        # print(xBlock,yBlock)
        if xBlock == xStart and yBlock == yStart:
            continue
        if mp[(xBlock,yBlock)] == '#':
            continue
        assert(mp[(xBlock,yBlock)] == '.')

        # place temp obstruction
        mp[(xBlock,yBlock)] = '#'

        visits = set()
        x,y,dX,dY = xStart,yStart,dXStart,dYStart
        looped = False
        while True:

            xNext,yNext = x+dX,y+dY
            if (xNext,yNext) not in mp:
                break
            if mp[(xNext,yNext)] == "#":
                if (x,y,dX,dY) in visits:
                    looped = True
                    break
                visits.add((x,y,dX,dY))
                dX,dY = -dY,dX
            else:
                x,y = xNext,yNext

        # remove temp obstruction
        mp[(xBlock,yBlock)] = '.' 

        if looped:
            blockCount += 1

    print(blockCount)


# day6b(test6)
day6bv3(input6)
