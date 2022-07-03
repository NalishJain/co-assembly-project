import sys

def varsNotAtBeginning(i):
    sys.stdout.write(f'Error at line {i}: variable not defined at the beginning\n')
    sys.exit()

def varAlreadyExists(line_num):
    sys.stdout.write(f'Error at line {line_num}: variable already exists\n')
    sys.exit()

def checkVariable(inst, i, var_dict):
    if inst[2] in var_dict.keys():
        return
    else:
        sys.stdout.write(f'Error at line {i}: variable not defined\n')
        sys.exit()

def checkLabel(inst, i, label_dict):
    if inst[1] in label_dict.keys():
        return
    else:
        sys.stdout.write(f'Error at line {i}: label not defined\n')
        sys.exit()

def labelAlreadyExists(line_num):
    sys.stdout.write(f'Error at line {line_num}: label already exists\n')
    sys.exit()


def hltErrors(lst):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == []:
            continue
        if lst[i] != []:
            if len(lst[i]) == 1 :
                if lst[i][0] != "hlt":
                    sys.stdout.write(f'Error at line {i + 1}: Halt instruction not present at the end\n')
                    sys.exit()
                else:
                    flag = 1
                    t = i 
                    break
            if len(lst[i]) == 2 :
                if lst[i][1] != "hlt":
                    sys.stdout.write(f'Error at line {i + 1}: Halt instruction not present at the end\n')
                    sys.exit()
                else:
                    flag = 1
                    t = i 
                    break
            
    if flag == 1:
        for i in range(t - 1, -1, -1):
            if lst[i] == []:
                continue
            if len(lst[i]) == 1:
                if lst[i][0] == "hlt":
                    sys.stdout.write(f'Error at line {i + 1}: Multiple halt instructions present\n')
                    sys.exit()
            if len(lst[i]) == 2:
                if lst[i][1] == "hlt":
                    sys.stdout.write(f'Error at line {i + 1}: Multiple halt instructions present\n')
                    sys.exit()

                
def check_immediate(immediate, line_num):
    if (not (0 <= immediate <=255)):
        sys.stdout.write(f"Error: line {line_num}, The value of immediate {immediate} should be integer in range [0, 255]")
        sys.exit()

def check_reg(reg, rdict, line_num):
    if reg not in rdict:
        sys.stdout.write(f"Error: line {line_num}, register {reg} you are trying to access does not exist")
        sys.exit()

def check_opcode(ins, opCode, line_num):
    if ins not in opCode:
        sys.stdout.write(f"Error: line {line_num}, instruction {ins} does not exist")
        sys.exit()
