import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input3 import *

test3 = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

def day3a(s):
    total = 0
    for m in re.findall(r"mul\(([0-9]+),([0-9]+)\)", s):
        # print(m)
        total += int(m[0]) * int(m[1])
    print(total)

# day3a(test3)
# day3a(input3)

test3b="""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

def day3b(s):
    total = 0
    shouldDo = True
    for m in re.findall(r"(do\(\)|don't\(\)|mul\(([0-9]+),([0-9]+)\))", s):
        if m[0] == "do()":
            shouldDo = True
        elif m[0] == "don't()":
            shouldDo = False
        elif shouldDo:
            total += int(m[1]) * int(m[2])
    print(total)

# day3b(test3b)
day3b(input3)
