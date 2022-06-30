from utils import *
import sys

assembly_input = sys.stdin.read().split('\n')

init_lst = [i.split() for i in assembly_input]

lst = []
for i in init_lst:
    if i == []:
        continue
    lst.append(i)
print(lst)

code_length = len(lst)

i = 0
var_count = 0
while lst[i][0] == "var":
    var_count += 1
    i += 1

var_dict = {}
mem_addr = code_length - var_count
for i in lst[:var_count]:
    var_dict[i[1]] = bin(mem_addr)[2:]
    mem_addr += 1
print(var_dict)

def typeA(inst):
    s = get_opcode(inst[0]) + "00" + get_reg(inst[1]) + get_reg(inst[2]) + get_reg(inst[3])
    return s

def typeB(inst):
    opcode = get_opcode(inst[0]) if (inst[0]!="mov") else get_opcode("movi")
    immediate = bin(inst[2][1:])[2:]
    if (not (0 <= immediate <=255)):
        raise Exception(f"The value of immediate {immediate} should be integer in range [0, 255]")
    return opcode + get_reg(inst[1]) + ("0"*(8-len(immediate))) + immediate

def typeC(inst):
    opcode = get_opcode(inst[0]) if (inst[0]!="mov") else get_opcode("movr")
    if inst[0] == "mov" and inst[2] == "FLAGS":
        return opcode + "0"*5 + get_reg(inst[1]) + "111" #FLAGS at 111
    return opcode + "0"*5 + get_reg(inst[1]) + get_reg(inst[2])

def typeD(inst):
    opcode = get_opcode(inst[0])
    return opcode + get_reg(inst[1]) + ("0"*(8-len(var_dict[inst[2]]))) + var_dict[inst[2]]

def typeE(inst):
    pass

def typeF(inst):
    s = get_opcode[inst[0]] + "00000000000"
    return s

def convert(inst):

    if (inst[0] == "mov"):
        "FLAGS" : "110"
        if '$' in inst[2]:
            typeB(inst)
        else:
            typeC(inst)

    elif (get_opcode(inst[0]) in ["10000","10001","10110","11010" ,"11011","11100"]):
        s = typeA(inst)
    elif (get_opcode(inst[0]) in ["11001"]):
        s = typeB(inst)
    elif (get_opcode(inst[0]) in ["10111", "11101", "11110"]):
        s = typeC(inst)
    elif (get_opcode(inst[0]) in ["10101", "10100"]):
        s = typeD(inst)
    elif (get_opcode(inst[0]) in ["01111", "01101", "11111", "01100"]):
        s = typeE(inst)
    return s

binary_lst = []

for inst in lst[var_count:code_length-1]:
    print(inst)
    binary_lst.append(convert(inst))


