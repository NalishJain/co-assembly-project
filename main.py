from utils import *
import sys

assembly_input = sys.stdin.read().split('\n')

lst = [i.split() for i in assembly_input]

code_length = len(lst)-1

i = 0
var_count = 0
while lst[i][0] == "var":
    var_count += 1
    i += 1

for inst in lst[var_count:code_length]:
    pass
    # convert(inst)


def typeA(lst):
    s = get_opcode[lst[0]] + "00" + get_reg[lst[1]] + get_reg[lst[2]] + get_reg[lst[3]]
    return s


def typeB(lst):
    opcode = get_opcode(lst[0]) if (lst[0]!="mov") else get_opcode("mov_i")
    immediate = bin(lst[2][1:])[2:]
    if (not (0 <= immediate <=255)):
        raise Exception(f"The value of immediate {immediate} should be integer in range [0, 255]")
    return opcode + get_reg(lst[1]) + ("0"*(8-len(immediate))) + immediate


def typeC(lst):
    opcode = get_opcode(lst[0]) if (lst[0]!="mov") else get_opcode("mov_r")
    return opcode + "0"*5 + get_reg(lst[1]) + get_reg(lst[2])


def typeF(lst):
    s = get_opcode[lst[0]] + "00000000000"
    return s


if (get_opcode[lst[0]] in ["10000","10001","10110","11010" ,"11011","11100"]):
    s = typeA(lst)
elif (get_opcode[lst[0]] in ["11001", "10010"]):
    s = typeB(lst)
elif (get_opcode[lst[0]] in ["10011", "10111", "11101", "11110"]):
    s = typeC(lst)
elif (get_opcode[lst[0]] in ["10101", "10100"]):
    s = typeD(lst)
elif (get_opcode[lst[0]] in ["01111", "01101", "11111", "01100"]):
    s = typeE(lst)
else:
    s = typeF(lst)
