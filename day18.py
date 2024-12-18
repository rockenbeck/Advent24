import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq

from input18 import *

test18="""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

def day18a(s,dX,dY,cWall):

    bytes = []
    for line in s.split('\n'):
        bytes.append(tuple(map(int, line.split(','))))
        if len(bytes) == cWall:
            break

    mp = {}
    for byte in bytes:
        mp[byte] = '#'
    
    x,y = 0,0
    xEnd,yEnd = dX-1,dY-1
    back = {}
    e = [(0,0,0)]

    while len(e) > 0:
        x,y,l = e.pop(0)
        for diX,diY in [(-1,0),(1,0),(0,-1),(0,1)]:
            xN,yN = x+diX,y+diY
            lN = l + 1
            if xN == xEnd and yN == yEnd:
                print(f"found len {lN}")
                return
            if xN < 0 or xN >= dX or yN < 0 or yN >= dY:
                continue
            if (xN,yN) in mp:
                continue
            if (xN,yN) in back:
                continue
            back[(xN,yN)] = (x,y,l)
            e.append((xN,yN,lN))
    sD = ""
    for y in range(dY):
        for x in range(dX):
            if (x,y) in mp:
                sD += '#'
            elif (x,y) in back:
                sD += 'O'
            else:
                sD += '.'
        sD += '\n'
    print(sD)

# day18a(test18,7,7,12)
# day18a(input18,71,71,1024)

def hasPath(mp,dX,dY):
    x,y = 0,0
    xEnd,yEnd = dX-1,dY-1
    back = {}
    e = [(0,0,0)]

    while len(e) > 0:
        x,y,l = e.pop(0)
        for diX,diY in [(-1,0),(1,0),(0,-1),(0,1)]:
            xN,yN = x+diX,y+diY
            lN = l + 1
            if xN == xEnd and yN == yEnd:
                # print(f"found len {lN}")
                return True
            if xN < 0 or xN >= dX or yN < 0 or yN >= dY:
                continue
            if (xN,yN) in mp:
                continue
            if (xN,yN) in back:
                continue
            back[(xN,yN)] = (x,y,l)
            e.append((xN,yN,lN))
            
    return False

def day18b(s,dX,dY):
    bytes = []
    for line in s.split('\n'):
        bytes.append(tuple(map(int, line.split(','))))

    # Brute-force: rebuild map fresh up to N bytes, check for path
    # A much faster version would find a path, then drop bytes until one
    # lands on that path, then check for a new path. What would be faster?
    
    for i in range(1,len(bytes)):
        mp = {}
        for byte in bytes[:i]:
            mp[byte] = '#'
        if not hasPath(mp,dX,dY):
            print(f"no path after dropping {i} bytes, last at {bytes[i-1]}")
            return
    assert(False)


# day18b(test18,7,7)
day18b(input18,71,71)
