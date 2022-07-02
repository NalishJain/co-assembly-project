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
