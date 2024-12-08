import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input8 import *

test8="""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

def parse(s):
    mp = {}
    ants = []
    yMax = 0
    for line in s.split('\n'):
        xMax = 0
        for ch in line:
            mp[(xMax,yMax)] = ch
            if ch != '.':
                ants.append((xMax,yMax,ch))
            xMax += 1
        yMax += 1
    return ants,xMax,yMax,mp
    
def day8a(s):
    ants,xMax,yMax,mp = parse(s)

    mpFreqAPos = defaultdict(list)
    for ant in ants:
        mpFreqAPos[ant[2]].append((ant[0],ant[1]))
    # print(mpFreqAPos)

    antinodes = set()
    for freq,aPos in mpFreqAPos.items():
        # print(freq,aPos)
        for i in range(len(aPos) - 1):
            for j in range(i+1,len(aPos)):
                antinode0 = (2*aPos[j][0] - aPos[i][0], 2*aPos[j][1] - aPos[i][1])
                antinode1 = (2*aPos[i][0] - aPos[j][0], 2*aPos[i][1] - aPos[j][1])
                for antinode in (antinode0,antinode1):
                    if antinode[0] < 0 or antinode[0] >= xMax:
                        continue
                    if antinode[1] < 0 or antinode[1] >= yMax:
                        continue
                    antinodes.add(antinode)
    # print(antinodes)
    print(len(antinodes))

# day8a(test8)
# day8a(input8)


def day8b(s):
    ants,xMax,yMax,mp = parse(s)

    mpFreqAPos = defaultdict(list)
    for ant in ants:
        mpFreqAPos[ant[2]].append((ant[0],ant[1]))

    antinodes = set()
    for freq,aPos in mpFreqAPos.items():
        for i in range(len(aPos) - 1):
            for j in range(i+1,len(aPos)):
                dX,dY = aPos[j][0] - aPos[i][0], aPos[j][1] - aPos[i][1]
                for dir in (-1,1):
                    l = 0
                    while True:
                        x,y = (l*dir*dX + aPos[i][0], l*dir*dY + aPos[i][1])
                        if x < 0 or x >= xMax:
                            break
                        if y < 0 or y >= yMax:
                            break
                        antinodes.add((x,y))
                        l += 1
    # print(antinodes)
    s = ""
    for y in range(yMax):
        for x in range(xMax):
            if mp[(x,y)] == '.' and (x,y) in antinodes:
                s += '#'
            else:
                s += mp[(x,y)]
        s += '\n'
    # print(s)
    print(len(antinodes))

# day8b(test8)
day8b(input8)
