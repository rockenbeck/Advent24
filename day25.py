import re
from collections import defaultdict
# import sys
# import random
# import math
# import numpy as np
import heapq

from input25 import *

def day25a(s):

    keys = []
    locks = []

    for blocks in s.split('\n\n'):

        # build map from (x,y) to char at that location 
        mp = defaultdict(lambda:"")
        y = 0
        for line in blocks.split('\n'):
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

        assert(x==5)
        assert(y==7)

        # parse map; could do this all faster by building it directly with a single pass,
        # or without the dictionaries
        
        ah = []
        if mp[(0,0)] == '#':
            #lock
            for x in range(5):
                for y in range(1,7):
                    if mp[(x,y)] == '.':
                        ah.append(y-1)
                        break
            assert(len(ah) == 5)
            locks.append(ah)
        else: 
            #key
            assert(mp[(0,0)] == '.')
            for x in range(5):
                for y in range(5,-1,-1):
                    if mp[(x,y)] == '.':
                        ah.append(5 - y)
                        break

            assert(len(ah) == 5)
            keys.append(ah)

    # print(keys)
    # print(locks)

    total = 0
    for key in keys:
        for lock in locks:
            fit = True
            for x in range(5):
                if key[x] + lock[x] > 5:
                    fit = False
                    break
            if fit:
                total += 1

    print(f"total = {total}")

# day25a(test25)
day25a(input25)

# There's usually not a 25B, and that's again the case, so done!