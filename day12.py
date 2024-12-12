import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input12 import *

test12="""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

def parse(s):
    # build map from (x,y) to char at that location
    mp = defaultdict(lambda:"")
    yMax = 0
    for line in s.split('\n'):
        xMax = 0
        for ch in line:
            mp[(xMax,yMax)] = ch
            xMax += 1
        yMax += 1
    return xMax,yMax,mp

def root(x,y,conn):
    # run up linked list to root
    while True:
        xNext,yNext = conn[(x,y)]
        if xNext==x and yNext==y:
            xRoot,yRoot = x,y
            break
        x,y = xNext,yNext

    # do it again, pointing every one along the way at root
    # works without, but this is usually much faster
    while True:
        xNext,yNext = conn[(x,y)]
        if xNext==xRoot and yNext==yRoot:
            break
        conn[(x,y)] = (xRoot,yRoot)
        x,y = xNext,yNext

    return (xRoot,yRoot)
    
def tryconnect(x0,y0,x1,y1,mp,conn):
    assert((x0,y0) in conn)
    
    # connect adjacent if same char
    if mp[(x0,y0)] == mp[(x1,y1)]:
        xRoot0,yRoot0 = root(x0,y0,conn)
        xRoot1,yRoot1 = root(x1,y1,conn)
        conn[(xRoot1,yRoot1)] = (xRoot0,yRoot0)

def nsew(x, y):
    return [(x,y-1),(x,y+1),(x+1,y),(x-1,y)]

def connections(xMax,yMax,mp):
    conn = {}

    # init with each location pointing at itself
    for y in range(yMax):
        for x in range(xMax):
            conn[(x,y)] = (x,y)

    # connect regions
    for y in range(yMax):
        for x in range(xMax):
            for x1,y1 in nsew(x,y):
                tryconnect(x,y,x1,y1,mp,conn)

    # root(x,y,conn) is now the same for each location in connected set

    return conn

def day12a(s):
    xMax,yMax,mp = parse(s)

    conn = connections(xMax,yMax,mp)

    mprootareaperim = defaultdict(lambda:(0,0))

    for y in range(yMax):
        for x in range(xMax):
            # count cell's edges
            edges = 0
            ch = mp[(x,y)]
            for x1,y1 in nsew(x,y):
                if mp[(x1,y1)] != ch:
                    edges += 1
            # attribute each edge and cell to region's root
            xRoot,yRoot = root(x,y,conn)
            ap = mprootareaperim[(xRoot,yRoot)]
            mprootareaperim[(xRoot,yRoot)] = (ap[0] + 1, ap[1]+edges)

    total = 0
    for xRoot,yRoot in mprootareaperim.keys():
        ch = mp[(xRoot,yRoot)]
        ap = mprootareaperim[(xRoot,yRoot)]
        # print(f"A region of {ch} plants with price {ap[0]} * {ap[1]} = {ap[0] * ap[1]}.")
        total += ap[0] * ap[1]

    print(f"total = {total}")

# day12a(test12)
# day12a(input12)

def day12b(s):
    xMax,yMax,mp = parse(s)

    conn = connections(xMax, yMax, mp)

    mprootsidesperim = defaultdict(lambda:(0,0))

    for y in range(yMax):
        for x in range(xMax):
            # region (polygon) has same number of corners as sides, and corners
            #  are easier to count
            corners = 0
            ch = mp[(x,y)]
            for x1,y1 in [(x-1,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1)]:
                if mp[(x,y1)] != ch and mp[(x1,y)] != ch:
                    corners += 1 # outside corner
                if mp[(x,y1)] == ch and mp[(x1,y)] == ch and mp[(x1,y1)] != ch:
                    corners += 1 # inside corner
            
            # attribute each edge and sides=corners to region's root
            xRoot,yRoot = root(x,y,conn)
            ap = mprootsidesperim[(xRoot,yRoot)]
            mprootsidesperim[(xRoot,yRoot)] = (ap[0] + 1, ap[1]+corners)

    total = 0
    for xRoot,yRoot in mprootsidesperim.keys():
        ch = mp[(xRoot,yRoot)]
        ap = mprootsidesperim[(xRoot,yRoot)]
        # print(f"A region of {ch} plants with price {ap[0]} * {ap[1]} = {ap[0] * ap[1]}.")
        total += ap[0] * ap[1]

    print(f"total = {total}")

# day12b(test12)
day12b(input12)
