import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input13 import *

test13="""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

def day13a(s):
    # Somewhat disappointingly, the given machines always have button A and button B
    #  pointing in non-parallel directions, so there's only a single possible solution,
    #  which is trivial to find with Cramer's method, and all that needs to be verified
    #  is whether the solution consists of integers. No "cheapest" required.
    # I expected inputs like (1,1) and (3,3) with prize at (10,10).
    # The mention of hexagonal tiles also made me expect that this would be on a
    #  hexagonal grid (which only changes the math slightly)

    total = 0
    for block in s.split("\n\n"):
        lines = list(block.split("\n"))
        m = re.match(r"Button A: X\+([0-9]+), Y\+([0-9]+)", lines[0])
        xA,yA = map(int,m.groups())
        m = re.match(r"Button B: X\+([0-9]+), Y\+([0-9]+)", lines[1])
        xB,yB = map(int,m.groups())
        m = re.match(r"Prize: X=([0-9]+), Y=([0-9]+)", lines[2])
        xPrize,yPrize = map(int,m.groups())

        xPrize += 10000000000000 # part B
        yPrize += 10000000000000

        # solve cA * (xA,yA) + cB * (xB,yB) = (xPrize,yPrize) using Cramer's rule

        d = xA * yB - xB * yA
        if d == 0:
            assert(False) # parallel buttons. Not handled because not in inputs
        else:
            cA = (xPrize * yB - xB * yPrize) / d
            cB = (xA * yPrize - xPrize * yA) / d
            if cA != int(cA) or cB != int(cB):
                pass # no integer solution
            elif cA < 0 or cB < 0:
                pass # no non-negative solution (surprisingly never occurs in inputs)
            else:
                total += 3 * int(cA) + int(cB) # cheapest solution because only solution
    print(f"total = {total}")

# day13a(test13)
day13a(input13)
