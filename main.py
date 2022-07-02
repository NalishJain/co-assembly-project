from utils import *
import sys
import errors

# all errors should be defined in errors.py to distinguish them from normal util funcs

assembly_input = sys.stdin.read().split('\n')

init_lst = [i.split() for i in assembly_input][:-1]
print(init_lst)

var_count = 0
label_count = 0
inst_count = 0
var_flag = False
for i in range(len(init_lst)):
    if init_lst[i] == []:
        continue
    elif init_lst[i][0] == 'var':
        if var_flag == True:
          errors.varsNotAtBeginning(i+1)
        var_count += 1
    elif init_lst[i][0][-1] == ':':
        label_count += 1
        var_flag = True
        inst_count += 1
    else:
        var_flag = True
        inst_count += 1


errors.hltErrors(init_lst)

# Creating dictionary for variables
var_dict = {}
mem_addr = inst_count
line_num = 1
for i in init_lst:
    if i == []:
        line_num += 1
        continue
    if i[0] == 'var':
        if i[1] in var_dict.keys():
            errors.varAlreadyExists(line_num)
        var_dict[i[1]] = bin(mem_addr)[2:]
        mem_addr += 1
    line_num += 1

print(var_dict)

# Creating dictionary for labels
label_dict = {}
mem_addr = 0
line_num = 1
for inst in init_lst:
    if inst == [] or inst[0] == 'var':
        line_num += 1
        continue
    if inst[0][-1] == ':':
        if inst[1] in label_dict.keys():
            errors.labelAlreadyExists(line_num)
        label_dict[inst[0][:-1]] = bin(mem_addr)[2:]
    mem_addr += 1
    line_num += 1

print(label_dict)



def typeA(inst, line_num):
    s = get_opcode(inst[0], line_num) + "00" + get_reg(inst[1], line_num) + get_reg(inst[2], line_num) + get_reg(inst[3], line_num)
    return s

def typeB(inst, line_num):
    opcode = get_opcode(inst[0], line_num) if (inst[0]!="mov") else get_opcode("movi", line_num)
    immediate = bin(inst[2][1:])[2:]
    errors.check_immediate(immediate, line_num)
    return opcode + get_reg(inst[1], line_num) + ("0"*(8-len(immediate))) + immediate

def typeC(inst, line_num):
    opcode = get_opcode(inst[0], line_num) if (inst[0]!="mov") else get_opcode("movr", line_num)
    if inst[0] == "mov" and inst[2] == "FLAGS":
        return opcode + "0"*5 + get_reg(inst[1], line_num) + "111" #FLAGS at 111
    return opcode + "0"*5 + get_reg(inst[1], line_num) + get_reg(inst[2], line_num)

def typeD(inst, line_num):
    opcode = get_opcode(inst[0], line_num)
    errors.checkVariable(inst, line_num, var_dict)
    return opcode + get_reg(inst[1], line_num) + ("0"*(8-len(var_dict[inst[2]]))) + var_dict[inst[2]]

def typeE(inst, line_num):
    opcode = get_opcode(inst[0], line_num)
    errors.checkLabel(inst, line_num, label_dict)
    return opcode + "000" + ("0"*(8-len(label_dict[inst[1]]))) + label_dict[inst[1]]

def typeF(inst, line_num):
    s = get_opcode(inst[0], line_num) + "00000000000"
    return s

def convert(inst, line_num):

    if (inst[0] == "mov"):
        # "FLAGS" : "110"
        if '$' in inst[2]:
            typeB(inst)
        else:
            typeC(inst)

    elif (get_opcode(inst[0], line_num) in ["10000","10001","10110","11010" ,"11011","11100"]):
        s = typeA(inst, line_num)
    elif (get_opcode(inst[0], line_num) in ["11001"]):
        s = typeB(inst, line_num)
    elif (get_opcode(inst[0], line_num) in ["10111", "11101", "11110"]):
        s = typeC(inst, line_num)
    elif (get_opcode(inst[0], line_num) in ["10101", "10100"]):
        s = typeD(inst, line_num)
    elif (get_opcode(inst[0], line_num) in ["01111", "01101", "11111", "01100"]):
        s = typeE(inst, line_num)
    elif (get_opcode(inst[0], line_num) == "01010"):
        s = typeF(inst, line_num)
    return s

binary_lst = []
line_num = 1
for inst in init_lst:
    if inst != [] and inst[0] != 'var':
        if inst[0][-1] == ':':
            binary_lst.append(convert(inst[1:], line_num))
        else:
            binary_lst.append(convert(inst, line_num))
    line_num += 1

# for i in binary_lst:
#     print(i)

for i in binary_lst:
    sys.stdout.write(i+'\n')
