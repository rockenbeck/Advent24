import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input10 import *

test10="""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

def parse(s):
    mp = {}
    heads = []
    yMax = 0
    for line in s.split('\n'):
        xMax = 0
        for ch in line:
            n = int(ch)
            mp[(xMax,yMax)] = n
            if n == 0:
                heads.append((xMax,yMax))
            xMax += 1
        yMax += 1
    return xMax,yMax,mp,heads

def addNines(mp,x,y,n,nines):
    nNext = n + 1
    rating = 0
    for dX,dY in [(0,-1),(0,1),(1,0),(-1,0)]:
        xT,yT = x+dX,y+dY
        if (xT,yT) not in mp:
            continue
        if mp[(xT,yT)] == nNext:
            if nNext == 9:
                nines.add((xT,yT))
                rating += 1
            else:
                rating += addNines(mp,xT,yT,nNext,nines)
    return rating

def day10(s):
    xMax,yMax,mp,heads = parse(s)

    scores = 0
    ratings = 0
    for x,y in heads:
        nines = set()
        ratings += addNines(mp,x,y,0,nines)
        scores += len(nines)

    print(f"scores = {scores}, ratings = {ratings}")

# day10(test10)
day10(input10)

