import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq

from input21 import *

test21="""029A
980A
179A
456A
379A"""

# 7 8 9
# 4 5 6
# 1 2 3
#   0 A

mpKeyPressNextNumeric = defaultdict(lambda:None, [
    (('7', '>'), '8'),
    (('7', 'v'), '4'),
    (('8', '<'), '7'),
    (('8', '>'), '9'),
    (('8', 'v'), '5'),
    (('9', '<'), '8'),
    (('9', 'v'), '6'),
    (('4', '^'), '7'),
    (('4', '>'), '5'),
    (('4', 'v'), '1'),
    (('5', '^'), '8'),
    (('5', '<'), '4'),
    (('5', '>'), '6'),
    (('5', 'v'), '2'),
    (('6', '^'), '9'),
    (('6', '<'), '5'),
    (('6', 'v'), '3'),
    (('1', '^'), '4'),
    (('1', '>'), '2'),
    (('2', '^'), '5'),
    (('2', '<'), '1'),
    (('2', '>'), '3'),
    (('2', 'v'), '0'),
    (('3', '^'), '6'),
    (('3', '<'), '2'),
    (('3', 'v'), 'A'),
    (('0', '^'), '2'),
    (('0', '>'), 'A'),
    (('A', '^'), '3'),
    (('A', '<'), '0')
])

#   ^ A
# < v >

mpKeyPressNextDirectional = defaultdict(lambda:None, [
    (('^', '>'), 'A'),
    (('^', 'v'), 'v'),
    (('A', '<'), '^'),
    (('A', 'v'), '>'),
    (('<', '>'), 'v'),
    (('v', '^'), '^'),
    (('v', '<'), '<'),
    (('v', '>'), '>'),
    (('>', '^'), 'A'),
    (('>', '<'), 'v')
])

def pushq(a,key1,key2,key3,i,presses):
    # can do a lot better than this, but sort of hard
    score = -i + len(presses)
    heapq.heappush(a, (score,key1,key2,key3,i,presses))

def day21a(s):
    total = 0
    for code in s.split('\n'):
        key1 = 'A'      # position of first robot's arm on numeric keypad
        key2 = 'A'      # position of second robot's arm on directional keypad
        key3 = 'A'      # position of third robot's arm on directional keypad
        i = 0           # how many digits first robot has already typed on numeric keypad
        presses = ""    # keys we've already pressed on directional keypad
        score = i       # order in which to expand states should include penalty for more presses

        best = defaultdict(None)

        # priority queue of states
        a = [(score,key1,key2,key3,i,presses)]

        pressesBest = None

        while len(a):
            score,key1,key2,key3,i,presses = heapq.heappop(a)

            if i == len(code):
                # only necessarily true if score is conservative (A*)
                pressesBest = presses
                break
            
            if (key1,key2,key3,i) in best and len(best[(key1,key2,key3,i)]) <= len(presses):
                continue # better not to have pushed it
            best[(key1,key2,key3,i)] = presses

            if key3 == 'A':
                if key2 == 'A':
                    if key1 == code[i]:
                        pushq(a,key1,key2,key3,i+1,presses + 'A')
                    # else pointing at wrong key for code
                else:
                    key1N = mpKeyPressNextNumeric[(key1,key2)]
                    if key1N != None:
                        pushq(a,key1N,key2,key3,i,presses + 'A')
            else:
                key2N = mpKeyPressNextDirectional[(key2,key3)]
                if key2N != None:
                    pushq(a,key1,key2N,key3,i,presses + 'A')

            for press in "^<>vA":
                key3N = mpKeyPressNextDirectional[(key3,press)]
                if key3N != None:
                    pushq(a,key1,key2,key3N,i,presses + press)

        total += int(code[:-1]) * len(pressesBest)
        print(f"{code}: {pressesBest}, complexity = {len(pressesBest) * int(code[:-1])} = {len(pressesBest)} * {int(code[:-1])}")

    print(f"total = {total}")

# day21a(test21)
# day21a(input21)

# def day21b(s):
#     N = 25 # might retrofit this to part A if it works
#     # there's no way brute force will work, is there?

#     total = 0
#     for code in s.split('\n'):
#         keys = ['A'] * N    # position of robots' arms on keypads
#         i = 0               # how many digits first robot has already typed on numeric keypad
#         presses = ""        # keys we've already pressed on directional keypad
#         score = i           # order in which to expand states should include penalty for more presses

#         best = defaultdict(None)

#         # priority queue of states
#         a = [(score,keys,i,presses)]

#         pressesBest = None

#           could continue to convert key1,key2,key3 to keys, but doesn't seem worth it


# 7 8 9
# 4 5 6
# 1 2 3
#   0 A

# On reflection, this dict is really probably not the best way to do this
# The order of keys in the presses matters - some are cheaper than others to get a robot to press!
# But that order may depend on the level within the robot hierarchy

mpFromToPressesNumeric = defaultdict(lambda:"", [
                     ('78', '>'),    ('79', '>>'),   ('74', 'v'),    ('75', 'v>'),  ('76', 'v>>'), ('71', 'vv'),   ('72', 'vv>'), ('73', 'vv>>'), ('70', '>vvv'), ('7A', '>>vvv'),
    ('87', '<'),                     ('89', '>'),    ('84', '<v'),   ('85', 'v'),   ('86', 'v>'),  ('81', '<vv'),  ('82', 'vv'),  ('83', 'vv>'),  ('80', 'vvv'),  ('8A', 'vvv>'),
    ('97', '<<'),    ('98', '<'),                    ('94', '<<v'),  ('95', '<v'),  ('96', 'v'),   ('91', '<<vv'), ('92', '<vv'), ('93', 'vv'),   ('90', '<vvv'), ('9A', 'vvv'),
    ('47', '^'),     ('48', '^>'),   ('49', '^>>'),                  ('45', '>'),   ('46', '>>'),  ('41', 'v'),    ('42', 'v>'),  ('43', 'v>>'),  ('40', '>vv'),  ('4A', '>>vv'),
    ('57', '<^'),    ('58', '^'),    ('59', '^>'),   ('54', '<'),                   ('56', '>'),   ('51', '<v'),   ('52', 'v'),   ('53', 'v>'),   ('50', 'vv'),   ('5A', 'vv>'),
    ('67', '<<^'),   ('68', '<^'),   ('69', '^'),    ('64', '<<'),   ('65', '<'),                  ('61', '<<v'),  ('62', '<v'),  ('63', 'v'),    ('60', '<vv'),  ('6A', 'vv'),
    ('17', '^^'),    ('18', '^^>'),  ('19', '^^>>'), ('14', '^'),    ('15', '^>'),  ('16', '^>>'),                 ('12', '>'),   ('13', '>>'),   ('10', '>v'),   ('1A', '>>v'),
    ('27', '<^^'),   ('28', '^^'),   ('29', '^^>'),  ('24', '<^'),   ('25', '^'),   ('26', '^>'),  ('21', '<'),                   ('23', '>'),    ('20', 'v'),    ('2A', 'v>'),
    ('37', '<<^^'),  ('38', '<^^'),  ('39', '^^'),   ('34', '<<^'),  ('35', '<^'),  ('36', '^'),   ('31', '<<'),   ('32', '<'),                   ('30', '<v'),   ('3A', 'v'),
    ('07', '^^^<'),  ('08', '^^^'),  ('09', '^^^>'), ('04', '^^<'),  ('05', '^^'),  ('06', '^^>'), ('01', '^<'),   ('02', '^'),   ('03', '^>'),                   ('0A', '>'),
    ('A7', '^^^<<'), ('A8', '<^^^'), ('A9', '^^^'),  ('A4', '^^<<'), ('A5', '<^^'), ('A6', '^^'),  ('A1', '^<<'),  ('A2', '<^'),  ('A3', '^'),    ('A0', '<')
])

#   ^ A
# < v >
mpFromToPressesDirectional = defaultdict(lambda:"", [
                  ('^A', '>'),   ('^<', 'v<'),  ('^v', 'v'),  ('^>', 'v>'), 
    ('A^', '<'),                 ('A<', 'v<<'), ('Av', '<v'), ('A>', 'v'), 
    ('<^', '>^'), ('<A', '>>^'),                ('<v', '>'),  ('<>', '>>'), 
    ('v^', '^'),  ('vA', '>^'),  ('v<', '<'),                 ('v>', '>'), 
    ('>^', '<^'), ('>A', '^'),   ('><', '<<'),  ('>v', '<')
])

# Never got this whole section to work, perhaps because different levels of hierarchy
#  have different best orders in which to press keys to get from one key to the next

# def cpress(keys, N, h):
#     """how many keys need to be pressed by user to get robot at depth N"""
#     """to press the sequence of keys followed by A, assuming all robots up to depth N"""
#     """are at A"""

#     if N == 0:
#         return len(keys) + 1 # No more robots. I can just press the key

#     # memoize
#     if (keys, N) in h:
#         return h[(keys, N)]
    
#     keyCur = 'A'
#     cp = 0
#     for keyNext in keys + 'A':
#         keysToMove = mpFromToPressesDirectional[keyCur + keyNext]
#         cp += cpress(keysToMove, N - 1, h)
#         keyCur = keyNext
    
#     h[(keys, N)] = cp
#     return cp

# def pushqCheck(a,keys,i,cp,presses):
#     # can do a lot better than this, but sort of hard
#     score = -i + cp
#     heapq.heappush(a, (score,keys,i,cp,presses))

# def cPressCheck(code, N):
#     """brute-force A* search in hopes of finding bug in current solution"""

#     keys = 'A'*(N+1) # positions of robots' arms on keypads (numeric followed by directionals)
#     i = 0            # how many digits first robot has already typed on numeric keypad
#     cp = 0           # count of keys we've already pressed on directional keypad
#     presses = ""

#     best = defaultdict(None)

#     # priority queue of states
#     a = []
#     pushqCheck(a,keys,i,cp,presses)

#     cpBest = None

#     while len(a):
#         score,keys,i,cp,presses = heapq.heappop(a)

#         if i == len(code):
#             # only necessarily true if score is conservative (A*)
#             cpBest = cp
#             break
        
#         if (keys,i) in best and best[(keys,i)] <= cp:
#             continue # better not to have pushed it

#         best[(keys,i)] = cp

#         irobot = N-1
#         while irobot >= 0:
#             if keys[irobot+1] != 'A':
#                 break
#             irobot -= 1
#         if irobot == -1:
#             if keys[0] == code[i]:
#                 pushqCheck(a,keys,i+1,cp + 1,presses + 'A')
#             # else final robot pointing at wrong key for code
#         else:
#             if irobot == 0:
#                 keyN = mpKeyPressNextNumeric[(keys[irobot],keys[irobot+1])]
#             else:
#                 keyN = mpKeyPressNextDirectional[(keys[irobot],keys[irobot+1])]
                
#             if keyN != None:
#                 pushqCheck(a,keys[:irobot] + keyN + keys[irobot+1:],i,cp + 1,presses + 'A')

#         for keyToMove in "^<>v":
#             keyN = mpKeyPressNextDirectional[(keys[N],keyToMove)]
#             if keyN != None:
#                 pushqCheck(a,keys[:N] + keyN,i,cp + 1,presses+keyToMove)

#     return cpBest,presses

# def day21b(s, N):
#     h = {}

#     total = 0
#     for code in s.split('\n'):
#         keyCur = 'A'
#         cp = 0
#         for keyNext in code:
#             keysToMove = mpFromToPressesNumeric[keyCur + keyNext]
#             cp += cpress(keysToMove, N, h)
#             keyCur = keyNext

#         # nCode = int(code[:-1]) if code[-1]=='A' else 0
#         # print(f"{code}: complexity = {cp * nCode} = {cp} * {nCode}")
#         # total += cp * nCode

#         cpCheck,presses = cPressCheck(code, N)
#         if cpCheck != cp:
#             print(f"{code}:{N}: {'FAIL' if cpCheck != cp else 'OK'} check {cp} == {cpCheck} {presses}")
#             # assert(False)
#             return False

#     # print(f"total = {total}")
#     return True


def day21b(s, N):
    """This way finally worked. Build maps for best count to type each key"""
    """given previous location. These maps are different for each level of the hierarchy"""
    
    # User typing last robot's keyboard
    mpFromToC = {} 
    for keyFrom in '<>^vA':
        for keyTo in '<>^vA':
            # User can type any key directly for one keystroke
            mpFromToC[keyFrom + keyTo] = 1

    # Each intermediate robot typing on next robot's keyboard
    for n in range(N):
        mpFromToCPrev = mpFromToC
        mpFromToC = {}

        for keyFrom in '<>^vA':
            for keyTo in '<>^vA':
                presses = mpFromToPressesDirectional[keyFrom + keyTo]
                cpBest = None
                # Looking for best over all orderings, but best will always have all of one direction
                # followed by all of other direction (right?), so only need to consider two cases.
                # But don't consider cases which will take us through "dead key"
                ps = [presses]
                if not((keyFrom in "<" and keyTo in "^A") or (keyFrom in "^A" and keyTo in "<")):
                    ps.append(presses[::-1])
                for p in ps:
                    keyCur = 'A'
                    cp = 0
                    for keyNext in p + 'A':
                        cp += mpFromToCPrev[keyCur + keyNext]
                        keyCur = keyNext
                    if cpBest == None or cp < cpBest:
                        cpBest = cp
                mpFromToC[keyFrom + keyTo] = cpBest
        
        # print(f"{mpFromToC}\n")

    # final robot typing on final keyboard
    mpFromToCPrev = mpFromToC
    mpFromToC = {}
    for keyFrom in '0123456789A':
        for keyTo in '0123456789A':
            presses = mpFromToPressesNumeric[keyFrom + keyTo]
            cpBest = None
            ps = [presses]
            if not((keyFrom in "741" and keyTo in "0A") or (keyFrom in "0A" and keyTo in "741")):
                ps.append(presses[::-1])
            for p in ps:
                keyCur = 'A'
                cp = 0
                for keyNext in p + 'A':
                    cp += mpFromToCPrev[keyCur + keyNext]
                    keyCur = keyNext
                if cpBest == None or cp < cpBest:
                    cpBest = cp
            mpFromToC[keyFrom + keyTo] = cpBest

    # print(f"{mpFromToC}\n")

    total = 0
    for code in s.split('\n'):
        keyCur = 'A'
        cp = 0
        for keyNext in code:
            cp += mpFromToC[keyCur + keyNext]
            keyCur = keyNext

        nCode = int(code[:-1]) if code[-1]=='A' else 0
        print(f"{code}: complexity = {cp * nCode} = {cp} * {nCode}")
        total += cp * nCode

    print(f"total = {total}")
    return True

# day21b(test21,2) # same as part A
day21b(input21,25)

