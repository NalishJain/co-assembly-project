import sys

def varsNotAtBeginning(i):
    sys.stdout.write(f'Error at line {i}: variable not defined at the beginning\n')
    sys.exit()

def varAlreadyExists(line_num):
    sys.stdout.write(f'Error at line {line_num}: variable already exists\n')
    sys.exit()

def varNotDefined(line_num):
    sys.stdout.write(f'Error at line {line_num}: variable not defined\n')
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

def labelNotDefined(line_num):
    sys.stdout.write(f'Error at line {line_num}: label not defined\n')
    sys.exit()


def hltErrors(lst):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == []:
            continue
        if lst[i] != []:
            if lst[i][0] != "hlt":
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
            if lst[i][0] == "hlt":
                sys.stdout.write(f'Error at line {i + 1}: Multiple halt instructions present\n')
                sys.exit()
                
