import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input15 import *

test15S="""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

def next(x,y,move):
    xNext,yNext = x,y
    if move == '^':
        yNext -= 1
    elif move == '>':
        xNext += 1
    elif move == 'v':
        yNext += 1
    else:
        assert(move == '<')
        xNext -= 1
    return xNext,yNext

def day15a(s):

    sMap,moves = s.split("\n\n")
    mp = {}
    yMax = 0
    for line in sMap.split('\n'):
        xMax = 0
        for ch in line:
            if ch == '@':
                xStart,yStart = xMax,yMax
                ch = '.'
            mp[(xMax,yMax)] = ch
            xMax += 1
        yMax += 1

    x,y = xStart,yStart
    for move in moves:
        if move == '\n':
            continue
        xNext,yNext = next(x,y,move)
        ch = mp[(xNext,yNext)]
        if ch == '.':
            x,y = xNext,yNext
            continue
        if ch == '#':
            continue
        assert(ch == 'O')
        xBox,yBox = xNext,yNext
        xT,yT = xBox,yBox
        while mp[(xT,yT)] == 'O':
            xT,yT = next(xT,yT,move)
        if mp[(xT,yT)] == '#':
            # boxes all the way against wall
            continue
        assert(mp[(xT,yT)] == '.')
        mp[(xT,yT)] = 'O'
        mp[(xBox,yBox)] = '.'
        x,y = xBox,yBox

    total = 0
    for y in range(yMax):
        for x in range(xMax):
            if mp[(x,y)] == 'O':
                total += y * 100 + x
    print(f"total = {total}")

# day15a(test15S)
# day15a(test15)
# day15a(input15)


def canmovebox(mp,x,y,move):
    ch = mp[(x,y)]
    if ch == '.':
        return True
    elif ch == '#':
        return False
    
    if ch == ']':
        x -= 1
    assert(mp[(x,y)] == '[')
    
    if move in '^v':
        xNext,yNext = next(x,y,move)
        if mp[(xNext,yNext)] == '[':
            return canmovebox(mp,xNext,yNext,move)
        else:
            return canmovebox(mp,xNext,yNext,move) and \
                   canmovebox(mp,xNext+1,yNext,move)
    elif move == '>':
        return canmovebox(mp,x+2,y,move)
    else:
        assert(move == '<')
        return canmovebox(mp,x-1,y,move)

def movebox(mp,x,y,move):
    ch = mp[(x,y)]
    assert(ch != '#')
    if ch == '.':
        return
    
    if ch == ']':
        x -= 1
    assert(mp[(x,y)] == '[')
    
    if move in '^v':
        xNext,yNext = next(x,y,move)
        if mp[(xNext,yNext)] == '[':
            movebox(mp,xNext,yNext,move)
        else:
            movebox(mp,xNext,yNext,move)
            movebox(mp,xNext+1,yNext,move)
        assert(mp[(xNext,yNext)] == '.')
        assert(mp[(xNext+1,yNext)] == '.')
        mp[(xNext,yNext)] = '['
        mp[(xNext+1,yNext)] = ']'
        mp[(x,y)] = '.'
        mp[(x+1,y)] = '.'
    elif move == '>':
        movebox(mp,x+2,y,move)
        assert(mp[(x+2,y)] == '.')
        mp[(x+2,y)] = ']'
        mp[(x+1,y)] = '['
        mp[(x,y)] = '.'
    else:
        assert(move == '<')
        movebox(mp,x-1,y,move)
        assert(mp[(x-1,y)] == '.')
        mp[(x-1,y)] = '['
        mp[(x,y)] = ']'
        mp[(x+1,y)] = '.'

def day15b(s):

    sMap,moves = s.split("\n\n")
    mp = {}
    yMax = 0
    for line in sMap.split('\n'):
        xMax = 0
        for ch in line:
            if ch == 'O':
                chNew = '[]'
            elif ch == '@':
                xStart,yStart = xMax,yMax
                chNew = '..'
            else:
                chNew = ch * 2 
            mp[(xMax,yMax)] = chNew[0]
            mp[(xMax+1,yMax)] = chNew[1]
            xMax += 2
        yMax += 1

    x,y = xStart,yStart
    for move in moves:

        # sMp = ""
        # for yT in range(yMax):
        #     for xT in range(xMax):
        #         if xT == x and yT == y:
        #             sMp += '@'
        #         else:
        #             sMp += mp[(xT,yT)]
        #     sMp += '\n'
        # print(f"{sMp}{move}") 

        if move == '\n':
            continue
        xNext,yNext = next(x,y,move)
        ch = mp[(xNext,yNext)]
        if ch == '.':
            x,y = xNext,yNext
            continue
        if ch == '#':
            continue
        assert(ch in '[]')
        if canmovebox(mp,xNext,yNext,move):
            movebox(mp,xNext,yNext,move)
            x,y = xNext,yNext         

    # sMp = ""
    # for yT in range(yMax):
    #     for xT in range(xMax):
    #         if xT == x and yT == y:
    #             sMp += '@'
    #         else:
    #             sMp += mp[(xT,yT)]
    #     sMp += '\n'
    # print(f"{sMp}") 
 
    total = 0
    for y in range(yMax):
        for x in range(xMax):
            if mp[(x,y)] == '[':
                total += y * 100 + x
    print(f"total = {total}")

test15b="""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

# day15b(test15b)
# day15b(test15L)
day15b(input15)
