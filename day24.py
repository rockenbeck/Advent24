# import re
from collections import defaultdict
# import sys
# import random
# import math
# import numpy as np
import heapq

from input24 import *

test24="""x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

class Gate:
    def __init__(self, name, nameIn0=None, op=None, nameIn1=None, val=None):
        self.name = Gate.mungeName(name)
        self.nameOrig = name
        self.nameIn0 = Gate.mungeName(nameIn0)
        self.in0 = None
        self.op = op
        self.nameIn1 = Gate.mungeName(nameIn1)
        self.in1 = None
        self.val = val

    def mungeName(name):
        if name == None or name[0] in "xy":
            return name
        else:
            return "_" + name

    def __repr__(self):
        if self.op == None:
             return f"{self.name}: {self.val}"
        else:
            return f"{self.in0.name} {self.op} {self.in1.name} -> {self.name}"

    def strOrig(self):
        if self.op == None:
            return f"{self.name}: {self.val}"
        else:
            return f"{self.in0.nameOrig} {self.op} {self.in1.nameOrig} -> {self.nameOrig}"

    def getVal(self,order=None):
        if self.val == None:
            assert(self.op != None)
            val0 = self.in0.getVal(order)
            val1 = self.in1.getVal(order)
            if self.op == "AND":
                self.val = val0 and val1
            elif self.op == "OR":
                self.val = val0 or val1
            elif self.op == "XOR":
                self.val = val0 ^ val1
            else:
                assert(False)
        assert(self.val == 0 or self.val == 1)
        if order != None and self.op != None:
            order.append(self)
        return self.val

def day24a(s):

    mpNameGate = {}

    sIns,sGates = s.split('\n\n')
    for line in sIns.split('\n'):
        name,val = line.split(':')
        val = int(val)
        assert(name not in mpNameGate)
        mpNameGate[name] = Gate(name,val=val)
        
    for line in sGates.split('\n'):
        # x00 AND y00 -> z00
        nameIn0,op,nameIn1,arrow,nameOut = line.split(' ')
        assert(nameOut not in mpNameGate)
        mpNameGate[nameOut] = Gate(nameOut,nameIn0,op,nameIn1)

    #resolve names
    for gate in mpNameGate.values():
        if gate.op != None:
            gate.in0 = mpNameGate[gate.nameIn0]
            gate.in1 = mpNameGate[gate.nameIn1]
            gate.nameIn0 = None
            gate.nameIn1 = None

    # should use list comprehension
    zs = []
    for name,gate in mpNameGate.items():
        if name[0] == 'z':
            zs.append(gate)

    zs.sort(key=lambda gate: gate.name, reverse=True)
    # print(zs)
    
    n = 0
    for gate in zs:
        n = (n << 1)
        n += gate.getVal()
    print(f"n = {n}")

# day24a(test24)
# day24a(input24)

def swapOutputs(mpNameGate, name0, name1):
    name0 = Gate.mungeName(name0)
    name1 = Gate.mungeName(name1)
    gate0 = mpNameGate[name0]
    gate1 = mpNameGate[name1]
    gate0.name = name1
    gate1.name = name0
    mpNameGate[gate0.name] = gate0
    mpNameGate[gate1.name] = gate1

def day24b(s):

    mpNameGate = {}

    sIns,sGates = s.split('\n\n')
    for line in sIns.split('\n'):
        name,val = line.split(':')
        val = int(val)
        assert(name not in mpNameGate)
        gate = Gate(name,val=val)
        mpNameGate[gate.name] = gate
        
    for line in sGates.split('\n'):
        # x00 AND y00 -> z00
        nameIn0,op,nameIn1,arrow,nameOut = line.split(' ')
        assert(nameOut not in mpNameGate)
        gate = Gate(nameOut,nameIn0,op,nameIn1)
        mpNameGate[gate.name] = gate

    # Found these by inspection of the sections of graph which had wrong "shape"
    # Sort of vague and one-off how I decided which ones to swap in each case
    # Unsatisfying result from a "write fun code" point of view
    swapOutputs(mpNameGate, "rkf", "z09")
    swapOutputs(mpNameGate, "jgb", "z20")
    swapOutputs(mpNameGate, "vcg", "z24")
    swapOutputs(mpNameGate, "rvc", "rrs")

    # jgb,rkf,rrs,rvc,vcg,z09,z20,z24 <= final answer

    gates = [gate for gate in mpNameGate.values() if gate.op != None]

    #resolve names
    for gate in gates:
        gate.in0 = mpNameGate[gate.nameIn0]
        gate.in1 = mpNameGate[gate.nameIn1]

    # We are given that the gates make an adder when connected correctly,
    #  so each xN, yN (which are labeled correctly) should have
    #     xN XOR yN -> oN       # first pass - oN label is correct (orig may be wrong)
    #     xN AND yN -> aN       # first pass - aN label is correct
    #     oN XOR cN-1 -> zN     # second pass - zN label may be wrong because input may be wrongly labeled
    #     oN AND cN-1 -> bN     # second pass
    #     aN OR bN -> cN        # third pass
    # zN+1 = cN

    # orig tcs is c09
    # swap z09/a09 orig rkf/z09
    # swap z20(orig jgb) / b20(orig z20)
    # swap z24(orig vcg)/c24(orig z24) 
    # swap a31/o32 orig rrs/mfq
    # _pgq OR o31(_rvc) -> _nsm: must be a31 OR b31 -> c31
    # swap _rvc/_rrs? Yes

    # new z20,z24,z09  wrong
    for gate in gates:
        n0 = gate.in0.name[1:]
        n1 = gate.in1.name[1:]
        if gate.op == "XOR" and gate.in0.name[0] in "xy" and gate.in1.name[0] in "xy":
            assert(n0 == n1)
            if n0 == '00':
                gate.name = "z" + n0
            else:
                gate.name = "o" + n0
        elif gate.op == "AND" and gate.in0.name[0] in "xy" and gate.in1.name[0] in "xy":
            assert(n0 == n1)
            if n0 == '00':
                gate.name = "c" + n0
            else:
                gate.name = "a" + n0

    for gate in gates:
        if gate.op == "XOR" and gate.in0.name[0] == 'o':
            gate.name = "z" + gate.in0.name[1:]
        elif gate.op == "XOR" and gate.in1.name[0] == 'o':
            gate.name = "z" + gate.in1.name[1:]
        elif gate.op == "AND" and gate.in0.name[0] == 'o':
            gate.name = "b" + gate.in0.name[1:]
        elif gate.op == "AND" and gate.in1.name[0] == 'o':
            gate.name = "b" + gate.in1.name[1:]

    for gate in gates:
        if gate.op == "OR" and gate.in0.name[0] == 'a':
            gate.name = "c" + gate.in0.name[1:]
        elif gate.op == "OR" and gate.in1.name[0] == 'a':
            gate.name = "c" + gate.in1.name[1:]

    for gate in gates:
        assert(gate.op != None)
        if gate.in0.name > gate.in1.name:
            gate.in0,gate.in1 = gate.in1,gate.in0

    order = sorted(gates, key=lambda gate: (gate.name[1:], gate.name))

    gatePrev = None
    for gate in order:
        assert(gate.op != None)
        if gatePrev != None and gate.name[1:] != gatePrev.name[1:]:
            print(' ')
        print(f"{gate}\t(orig {gate.strOrig()})")
        gatePrev = gate

    mpNameGateOrig = mpNameGate
    mpNameGate = defaultdict(lambda:"<not found>")
    for gate in gates:
        mpNameGate[gate.name] = gate

    for gate in order:
        assert(gate.op != None)

        if gate.name[0] in 'ao':
            continue # can't be wrong

        n = gate.name[1:]
        nameIn0 = None
        nameIn1 = None

        if gate.name[0] == 'b':
            nameIn0 = 'c' + f"{(int(n) - 1):02}"
            nameIn1 = 'o' + n

        elif gate.name[0] == 'z':
            if n == '00':
                nameIn0 = 'x' + n
                nameIn1 = 'y' + n
            else:
                nameIn0 = 'c' + f"{(int(n) - 1):02}"
                nameIn1 = 'o' + n

        elif gate.name[0] == 'c':
            if n == '00':
                nameIn0 = 'x' + n
                nameIn1 = 'y' + n
            else:
                nameIn0 = 'a' + n
                nameIn1 = 'b' + n

        if gate.in0.name != nameIn0 or gate.in1.name != nameIn1:
            if gate.in0.name == nameIn1 or gate.in1.name == nameIn0:
                gate.in0,gate.in1 = gate.in1,gate.in0
            print(f"WRONG {gate}: \tshould be {nameIn0} {gate.op} {nameIn1} -> {gate.name}")
            # (was {mpNameGate[nameIn0]})")
    
    print("\n")

    # print(f"gate a37 = {mpNameGate['a37']}")
    # gate a37 = y37 AND x37 -> a37 (orig y37 AND x37 -> trf))

    # zs = []
    # for gate in gates:
    #     if gate.nameOrig[0] == 'z':
    #         zs.append(gate)

    # zs.sort(key=lambda gate: gate.nameOrig, reverse=True)
    # # print(zs)

    # order = []
    # zs[0].getVal(order=order)
    # for gate in order:
    #     print(gate)

# day24b(test24)
day24b(input24)


