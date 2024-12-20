import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq

from input16 import *

test16="""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
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

def day16a(s):

    xMax,yMax,mp,xStart,yStart,xEnd,yEnd = parse(s)

    a = defaultdict(lambda : 1000000000)
    a[(xStart,yStart,'E')] = 0

    e = [(xStart,yStart,'E',0)]

    while True:
        if len(e) == 0:
            assert(False) # failed to find any path

        # way too expensive, even with Timsort?
        # look up Python priority queue again, or write my own
        # (used heapq below after finishing)

        e.sort(key = lambda n: n[3])

        x,y,dir,score = e.pop(0) # cheaper other way around?

        if dir == 'N':
            xNext,yNext = x,y-1
            dirs = ['E', 'W']
        elif dir == 'S':
            xNext,yNext = x,y+1
            dirs = ['W', 'E']
        elif dir == 'E':
            xNext,yNext = x+1,y
            dirs = ['S', 'N']
        else:
            xNext,yNext = x-1,y
            dirs = ['N', 'S']

        if mp[(xNext,yNext)] == '.':
            if score+1 < a[(xNext,yNext,dir)]:
                if (xNext,yNext) == (xEnd,yEnd):
                    scoreBest = score+1
                    break;
                a[(xNext,yNext,dir)] = score+1
                e.append((xNext,yNext,dir,score+1))

        for dirNext in dirs:
            if score+1000 < a[(x,y,dirNext)]:
                a[(x,y,dirNext)] = score+1000
                e.append((x,y,dirNext,score+1000))


    print(f"best score = {scoreBest}")

# day16a(test16)
# day16a(input16)


def day16b(s):

    xMax,yMax,mp,xStart,yStart,xEnd,yEnd = parse(s)

    a = defaultdict(lambda : 1000000000)

    # best score at each position
    a[(xStart,yStart,'E')] = 0

    # priority queue for best-first search
    e = [(0,xStart,yStart,'E')]

    # backpointers for finding best path(s)
    back = defaultdict(lambda : [])

    scoreBest = None

    while len(e):
        score,x,y,dir = heapq.heappop(e)

        if dir == 'N':
            xNext,yNext = x,y-1
            dirs = ['E', 'W']
        elif dir == 'S':
            xNext,yNext = x,y+1
            dirs = ['W', 'E']
        elif dir == 'E':
            xNext,yNext = x+1,y
            dirs = ['S', 'N']
        else:
            xNext,yNext = x-1,y
            dirs = ['N', 'S']

        # check forward if free
        if mp[(xNext,yNext)] == '.':
            scoreNext = score+1
            # stop if we're longer than best path(s)
            if scoreBest == None or scoreNext <= scoreBest:
                scoreCur = a[(xNext,yNext,dir)]
                if scoreNext <= scoreCur:
                    if (xNext,yNext) == (xEnd,yEnd):
                        scoreBest = scoreNext
                    a[(xNext,yNext,dir)] = scoreNext
                    heapq.heappush(e, (scoreNext,xNext,yNext,dir))
                    if scoreNext == scoreCur:
                        back[(xNext,yNext,dir)].append((x,y,dir))
                    else:
                        back[(xNext,yNext,dir)] = [(x,y,dir)]

        # check turn left/right
        for dirNext in dirs:
            scoreNext = score+1000
            if scoreBest == None or scoreNext <= scoreBest:
                scoreCur = a[(x,y,dirNext)];
                if scoreNext <= scoreCur:
                    a[(x,y,dirNext)] = scoreNext
                    heapq.heappush(e, (scoreNext,x,y,dirNext))
                    if scoreNext == scoreCur:
                        back[(x,y,dirNext)].append((x,y,dir))
                    else:
                        back[(x,y,dirNext)] = [(x,y,dir)]

    onPath = set()

    e = []
    for dir in "NSEW":
        e.append((xEnd,yEnd,dir))

    visited = set()
    
    while len(e) > 0:
        x,y,dir = e.pop()
        if (x,y,dir) in visited:
            continue
        visited.add((x,y,dir))
        onPath.add((x,y))
        e.extend(back[(x,y,dir)])

    print(f"on path = {len(onPath)}")


# day16b(test16)
day16b(input16)
