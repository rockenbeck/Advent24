import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq

from input20 import *

test20="""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""



def parse(s):
    # build map from (x,y) to char at that location
    
    mp = defaultdict(lambda:"")
    y = 0
    for line in s.split('\n'):
        x = 0
        for ch in line:
            if ch == "S":
                xStart,yStart = x,y
                ch = '.'
            elif ch == "E":
                xEnd,yEnd = x,y
                ch = '.'
            mp[(x,y)] = ch
            x += 1
        y += 1
    return x,y,mp,xStart,yStart,xEnd,yEnd


def day20(s,sSkipMax,sSaveMin):

    xMax,yMax,mp,xStart,yStart,xEnd,yEnd = parse(s)

    mpXYS = {}

    # best score at each position
    mpXYS[(xStart,yStart)] = 0

    # priority queue for best-first search
    # overkill if it's actually linear
    e = [(0,xStart,yStart)]

    while len(e):
        s,x,y = heapq.heappop(e)
        if (x,y) == (xEnd,yEnd):
            sTotal = s
            break;
        
        for diX,diY in [(-1,0),(1,0),(0,-1),(0,1)]:
            xN,yN = x+diX,y+diY
            sN = s+1

            if mp[(xN,yN)] != '.':
                continue
            if (xN,yN) in mpXYS:
                sCur = mpXYS[(xN,yN)]
                assert(sCur == s-1)
                continue

            mpXYS[(xN,yN)] = sN
            heapq.heappush(e, (sN,xN,yN))

    # print(f"sTotal = {sTotal}")

    mpSSaveC = defaultdict(lambda:0)

    # Solved part A with this
    # # Try removing every wall and see how much it saves
    # for y in range(1,yMax-1):
    #     for x in range(1,xMax-1):
    #         if mp[(x,y)] != '#':
    #             continue
    #         sSaveH = 0
    #         if mp[(x-1,y)] == '.' and mp[(x+1,y)] == '.':
    #             sSaveH = abs(mpXYS[(x-1,y)] - mpXYS[(x+1,y)]) - 2
    #         sSaveV = 0
    #         if mp[(x,y-1)] == '.' and mp[(x,y+1)] == '.':
    #             sSaveV = abs(mpXYS[(x,y-1)] - mpXYS[(x,y+1)]) - 2

    #         sSave = max(sSaveH,sSaveV)
    #         if sSave > 0:
    #             mpSSaveC[sSave] = mpSSaveC[sSave] + 1
    
    # Part B is more general
    # Try skip from every empty space to other empties in range and see how much it saves
    # Seems like there might be a yet faster way. E.g. this is checking each skip twice
    
    for y in range(1,yMax-1):
        for x in range(1,xMax-1):
            if mp[(x,y)] != '.':
                continue
            sStart = mpXYS[(x,y)]
            for dY in range(-sSkipMax,sSkipMax+1):
                for dX in range(-(sSkipMax - abs(dY)), sSkipMax - abs(dY) + 1):
                    sSkip = abs(dX) + abs(dY)
                    if sSkip < 2:
                        continue
                    xN,yN = x+dX,y+dY
                    if mp[(xN,yN)] == '.':
                        sSave = mpXYS[(xN,yN)] - sStart - sSkip
                        if sSave >= sSaveMin:
                            mpSSaveC[sSave] = mpSSaveC[sSave] + 1
    
    # print(mpSSaveC)
    saves = sorted([(c,sSave) for sSave,c in mpSSaveC.items()], key=lambda n: n[1])
    # print(saves)
    cTotal = 0
    for c,sSave in saves:
        cTotal += c

    print(f"{cTotal} cheats with len {sSkipMax} save at least {sSaveMin}ps")

def day20a(s,sSaveMin):
    day20(s,2,sSaveMin)

# day20a(test20,0)
# day20a(input20,100)

def day20b(s,sSaveMin):
    day20(s,20,sSaveMin)

# day20b(test20,50)
day20b(input20,100)
