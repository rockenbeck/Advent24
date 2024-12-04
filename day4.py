import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input4 import *

test4 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def day4a(s):
    grid = defaultdict(lambda : " ")
    y = 0
    for line in s.split('\n'):
        x = 0
        for ch in line:
            grid[(x,y)] = ch
            x += 1
        xMax = x
        y += 1
    yMax = y

    target = "XMAS"

    # brute-force search
    count = 0
    for y in range(yMax):
        for x in range(xMax):
            if grid[(x,y)] != target[0]:
                continue
            for dY in range(-1,2):
                for dX in range(-1,2):
                    if dX == 0 and dY == 0:
                        continue
                    found = True
                    for i in range(1,len(target)):
                        if grid[(x + i * dX, y + i * dY)] != target[i]:
                            found = False
                            break
                    if found:
                        count += 1
    print(count)

# day4a(test4)
# day4a(input4)

def day4b(s):
    grid = defaultdict(lambda : " ")
    y = 0
    for line in s.split('\n'):
        x = 0
        for ch in line:
            grid[(x,y)] = ch
            x += 1
        xMax = x
        y += 1
    yMax = y

    target = [((0,0), "A"), ((-1,-1), "M"), ((1,1), "S"), ((-1,1), "M"), ((1,-1), "S")]

    # brute-force search
    count = 0
    for y in range(yMax):
        for x in range(xMax):
            if grid[(x,y)] != target[0][1]:
                continue
            for mat in [(1,0,0,1),(0,-1,1,0),(-1,0,0,-1),(0,1,-1,0)]:
                found = True
                for t in target[1:]:
                    if grid[(x + t[0][0] * mat[0] + t[0][1] * mat[1], y + t[0][0] * mat[2] + t[0][1] * mat[3])] != t[1]:
                        found = False
                        break
                if found:
                    count += 1
    print(count)

# day4b(test4)
day4b(input4)
