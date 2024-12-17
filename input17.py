input17="""Register A: 60589763
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,1,6,4,1,5,5,0,3,3,0"""

# bst 4     b = a & 7
# bxl 5     b = b ^ 5
# cdv 5     c = a // (1 << b)
# bxl 6     b = b ^ 6
# bxc 1     b = b ^ c
# out 5     output(b & 7)
# adv 3     a = a // (1 << 3)
# jnz 0     if a != 0 goto 0

def test(a,b,c):
    while a != 0:
        b = (a & 7) ^ 5
        c = a // (1 << b)
        b = (b ^ 6) ^ c
        output(b & 7)
        a = a // 8

    #    if op == 0: # adv
    #         a = a // (1 << combo)
    #     elif op == 1: # bxl
    #         b = b ^ operand
    #     elif op == 2: # bst
    #         b = combo & 7
    #     elif op == 3: # jnz
    #         if a != 0:
    #             ip = operand
    #             continue
    #     elif op == 4: # bxc
    #         b = b ^ c
    #     elif op == 5: # out
    #         out.append(combo & 7)
    #         if len(out) > maxout:
    #             return out
    #     elif op == 6: # bdv
    #         b = a // (1 << combo)
    #     elif op == 7: # cdv
    #         c = a // (1 << combo)
