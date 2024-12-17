import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq

from input17 import *

test17="""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

def parse(s):

    m = re.match(r"Register A: ([0-9]+)\nRegister B: ([0-9]+)\nRegister C: ([0-9]+)\n\nProgram: ([0-9,]+)", s)
    a,b,c = map(int,m.groups()[0:3])
    prog = list(map(int, m.groups()[3].split(',')))

    return a,b,c,prog

def runprog(prog,a,b,c,check=False):

    ip = 0

    out = []
    iOut = 0

    while ip < len(prog):
        op = prog[ip]
        operand = prog[ip+1]
        combo = operand
        if combo == 4:
            combo = a
        elif combo == 5:
            combo = b
        elif combo == 6:
            combo = c
        elif combo == 7:
            assert(False)

        if op == 0: # adv
            a = a // (1 << combo)
        elif op == 1: # bxl
            b = b ^ operand
        elif op == 2: # bst
            b = combo & 7
        elif op == 3: # jnz
            if a != 0:
                ip = operand
                continue
        elif op == 4: # bxc
            b = b ^ c
        elif op == 5: # out
            n = combo & 7
            if check:
                if iOut >= len(prog) or n != prog[iOut]:
                    return None
                else:
                    iOut += 1
            else:
                out.append(n)
        elif op == 6: # bdv
            b = a // (1 << combo)
        elif op == 7: # cdv
            c = a // (1 << combo)

        ip += 2
    
    if check and iOut != len(prog):
        return None
    
    return out

def day17a(s):

    a,b,c,prog = parse(s)

    out = runprog(prog,a,b,c)

    print(",".join(map(str, out)))

# day17a(test17)
# day17a(input17)


test17b="""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

def runprogpy(prog,a,b,c,match):
    # given program converted into Python, which runs many times faster,
    #  but still not enough to easily yield to brute force

    iOut = 0
    out = []
    while True:
        b = (a & 7) ^ 5         # low octal digit ^ 5
        c = a // (1 << b)       # c = a >> b
        b = (b ^ 6) ^ c
        n = b & 7
        if match:
            if iOut >= len(prog) or n != prog[iOut]:
                return None
            else:
                iOut += 1
        else:
            out.append(n)
        a = a // 8
        if a == 0:
            break

    if match and iOut != len(prog):
        return None
    
    return out

def matchout(outA,outB):
    if len(outA) != len(outB):
        return False
    for i in range(len(outA)):
        if outA[i] != outB[i]:
            return False
    return True

def findA(prog,iO,aPrev):
    # return value of A which will produce program sequence starting from location iO,
    #  given aPrev, which produces sequence starting from iO + 1

    if iO < 0:
        return aPrev
    
    aThis = aPrev << 3
    o = prog[iO]

    for i in range(8):
        a = (aPrev << 3) + i
        b = i ^ 5
        b = (b ^ 6) ^ (a >> b)
        if (b & 7) == o:
            # Recurse to find next digits
            aFinal = findA(prog,iO-1,a)
            if aFinal != None:
                # print(f"{aFinal} => {runprogpy(prog,aFinal,0,0,False)}")
                return aFinal
            else:
                pass # didn't find full sequence, so continue to see if other digits here might work
    return None


def day17b(s):
    a,b,c,prog = parse(s)

    # brute force it? Nope!

    # # for a in range(1000000):
    # # for a in range(1000000,10000000):
    # # for a in range(10000000,100000000):
    # # for a in range(363800000,1000000000):
    # for a in range(1162600000,10000000000):
    #     if a % 100000 == 0:
    #         print(a)
    #     # outA = runprog(prog,a,b,c,False)
    #     # outB = runprogpy(prog,a,b,c,False)
    #     # if not matchout(outA, outB):
    #     #     print(f"match fail at A={a}, {outA}!={outB}")
    #     #     return
    #     if runprogpy(prog,a,b,c,True) != None:
    #         print(f"matches with A={a}")
    #         break
    # print("No match")

    # b = (a & 7) ^ 5           # b = low octal digit ^ 5
    # b = (b ^ 6) ^ (a >> b)    # 
    # n = b & 7
    # out.append(n)
    # a = a >> 3                # strip low octal digit

    # for a in range(8):
    #     outA = runprog(prog,a,b,c,False)
    #     print(f"{a}=>{outA}")

    # Add octal digits from the right, looking for one that will produce
    #  the next number in program
    # aFinal = 0
    # for iO in range(len(prog) - 1, -1, -1):
    #     o = prog[iO]
    # # for o in reversed(prog):
    #     aFinal = aFinal << 3
    #     aFound = None
    #     for i in range(8):
    #         a = aFinal + i
    #         if iO == 9:
    #             print(f"try {a} => {runprogpy(prog,a,b,c,False)}")
    #         b = i ^ 5
    #         b = (b ^ 6) ^ (a >> b)
    #         if (b & 7) == o:
    #             if aFound != None:
    #                 # lots of these, so can't just take first. Need to do search over tree of possibilities
    #                 print(f"{a} and {aFound} both produce {runprogpy(prog,a,b,c,False)}")
    #             aFound = a
    #     assert(aFound != None) # fails after a bit
    #     aFinal = aFound
    #     print(f"{aFinal} => {runprogpy(prog,aFinal,b,c,False)}")
        
    # This worked in the end, and is quite fast, but it was an awful lot of work to get here
    # I can't help thinking that I must have missed some much easier way to approach this problem.

    aFinal = findA(prog,len(prog) - 1,0)
    if aFinal != None:
        print(f"{aFinal} => {runprogpy(prog,aFinal,b,c,False)}")
    else:
        print("not found")

# day17b(test17b)
day17b(input17)
