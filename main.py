from utils import *
import sys
import errors

# all errors should be defined in errors.py to distinguish them from normal util funcs

line_num = 0
try:
    assembly_input = sys.stdin.read().split('\n')

    init_lst = [i.split() for i in assembly_input]
    # print(init_lst)


    errors.hltErrors(init_lst)

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
            if len(init_lst[i]) == 1:
                label_count += 1
                var_flag == True
            else:
                label_count += 1
                var_flag = True
                inst_count += 1
        else:
            var_flag = True
            inst_count += 1



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

    # print(var_dict)

    # Creating dictionary for labels
    label_dict = {}
    mem_addr = 0
    line_num = 1
    for inst in init_lst:
        if inst == [] or inst[0] == 'var':
            line_num += 1
            continue
        if inst[0][-1] == ':':
            if inst[0][:-1] in label_dict.keys():
                errors.labelAlreadyExists(line_num)
            if len(inst) == 1:
                label_dict[inst[0][:-1]] = bin(mem_addr)[2:]
            else:
                label_dict[inst[0][:-1]] = bin(mem_addr)[2:]
                mem_addr += 1
        else:
            mem_addr += 1
        line_num += 1
        # print(inst, line_num)

    # print(label_dict)
except SystemExit:
    print('Exiting...')
    sys.exit()
except:
    errors.genError(line_num)


def typeA(inst, line_num):
    inst_len = 4
    if len(inst) > inst_len:
        errors.tooManyArguments(line_num, inst_len, len(inst))
    if len(inst) < inst_len:
        errors.tooFewArguments(line_num, inst_len, len(inst))
    s = get_opcode(inst[0], line_num) + "00" + get_reg(inst[1], line_num) + get_reg(inst[2], line_num) + get_reg(inst[3], line_num)
    return s

def typeB(inst, line_num):
    inst_len = 3
    if len(inst) > inst_len:
        errors.tooManyArguments(line_num, inst_len, len(inst))
    if len(inst) < inst_len:
        errors.tooFewArguments(line_num, inst_len, len(inst))
    opcode = get_opcode(inst[0], line_num) if (inst[0]!="mov") else get_opcode("movi", line_num)
    immediate = bin(int(inst[2][1:]))[2:]
    errors.check_immediate(int(inst[2][1:]), line_num)
    return opcode + get_reg(inst[1], line_num) + ("0"*(8-len(immediate))) + immediate

def typeC(inst, line_num):
    inst_len = 3
    if len(inst) > inst_len:
        errors.tooManyArguments(line_num, inst_len, len(inst))
    if len(inst) < inst_len:
        errors.tooFewArguments(line_num, inst_len, len(inst))
    opcode = get_opcode(inst[0], line_num) if (inst[0]!="mov") else get_opcode("movr", line_num)
    if inst[0] == "mov" and inst[1] == "FLAGS":
        return opcode + "0"*5 + "111" + get_reg(inst[2], line_num) #FLAGS at 111
    return opcode + "0"*5 + get_reg(inst[1], line_num) + get_reg(inst[2], line_num)

def typeD(inst, line_num):
    inst_len = 3
    if len(inst) > inst_len:
        errors.tooManyArguments(line_num, inst_len, len(inst))
    if len(inst) < inst_len:
        errors.tooFewArguments(line_num, inst_len, len(inst))
    opcode = get_opcode(inst[0], line_num)
    errors.checkVariable(inst, line_num, var_dict)
    return opcode + get_reg(inst[1], line_num) + ("0"*(8-len(var_dict[inst[2]]))) + var_dict[inst[2]]

def typeE(inst, line_num):
    inst_len = 2
    if len(inst) > inst_len:
        errors.tooManyArguments(line_num, inst_len, len(inst))
    if len(inst) < inst_len:
        errors.tooFewArguments(line_num, inst_len, len(inst))
    opcode = get_opcode(inst[0], line_num)
    errors.checkLabel(inst, line_num, label_dict)
    return opcode + "000" + ("0"*(8-len(label_dict[inst[1]]))) + label_dict[inst[1]]

def typeF(inst, line_num):
    inst_len = 1
    if len(inst) > inst_len:
        errors.tooManyArguments(line_num, inst_len, len(inst))
    if len(inst) < inst_len:
        errors.tooFewArguments(line_num, inst_len, len(inst))
    s = get_opcode(inst[0], line_num) + "00000000000"
    return s

def convert(inst, line_num):
    # print(line_num)
    if (inst[0] == "mov"):
        if '$' in inst[2]:
            s = typeB(inst, line_num)
        else:
            s = typeC(inst, line_num)

    elif (get_opcode(inst[0], line_num) in ["10000", "10001", "10110", "11010" , "11011", "11100", "00000", "00001"]):
        s = typeA(inst, line_num)
    elif (get_opcode(inst[0], line_num) in ["11000", "11001"]):
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

try:
    binary_lst = []
    line_num = 1
    for inst in init_lst:
        if inst != [] and inst[0] != 'var':
            if inst[0][-1] == ':':
                if len(inst) == 1:
                    line_num+=1
                    continue
                binary_lst.append(convert(inst[1:], line_num))
            else:
                binary_lst.append(convert(inst, line_num))
        line_num += 1

    # for i in binary_lst:
    #     print(i)

    for i in binary_lst:
        sys.stdout.write(i+'\n')
except SystemExit:
    print('Exiting...')
    sys.exit()
except:
    errors.genError(line_num)
