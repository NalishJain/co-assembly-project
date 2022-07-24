import sys
# Flag variables

rdict = {
            "000": 0,
            "001": 0,
            "010": 0,
            "011": 0,
            "100": 0,
            "101": 0,
            "110": 0,
            "111": ['0','0','0','0']
        }

assembly_input = sys.stdin.read().split('\n')
init_lst = [i for i in assembly_input]
Memory = []

for i in range(256):
    Memory.append("0000000000000000")

for i in range(len(init_lst) - 1):
    Memory[i] = init_lst[i]

PC = 0
halted = False


def convertToDecimal(binary):
    d = int(binary,2)
    return d


def execute_typeA(Instruction):

    rdict["111"] = ['0','0','0','0']

    if  Instruction[0:5] == "10000":
        resA = rdict[Instruction[7:10]] + rdict[Instruction[10:13]]
        if resA < (2**16):
            rdict[Instruction[13:16]] = resA
        else:
            rdict["111"][0] = '1'
            rdict[Instruction[13:16]] = resA%(2**16)
    elif  Instruction[0:5] == "10000":
        resA = rdict[Instruction[7:10]] - rdict[Instruction[10:13]]
        if resA >= 0:
            rdict[Instruction[13:16]] = resA
        else:
            rdict["111"][0] = '1'
            rdict[Instruction[13:16]] = 0
    elif  Instruction[0:5] == "10110":
        resA = (rdict[Instruction[7:10]])*(rdict[Instruction[10:13]])
        if resA < (2**16):
            rdict[Instruction[13:16]] = resA
        else:
            rdict["111"][0] = '1'
            rdict[Instruction[13:16]] = resA%(2**16)

    elif  Instruction[0:5] == "11010":
        resA = (rdict[Instruction[7:10]])^(rdict[Instruction[10:13]])
        rdict[Instruction[13:16]] = resA

    elif  Instruction[0:5] == "11011":
        resA = (rdict[Instruction[7:10]])|(rdict[Instruction[10:13]])
        rdict[Instruction[13:16]] = resA

    else:
        resA = (rdict[Instruction[7:10]])&(rdict[Instruction[10:13]])
        rdict[Instruction[13:16]] = resA

def execute_typeB(Instruction):
    # reset flags
    rdict["111"] = ['0','0','0','0']

    reg = Instruction[5:8]
    imm = int(Instruction[8:], 2)
    inst = Instruction[0:5]
    if inst == "11000":
        rdict[reg] = rdict[reg] >> imm
    elif inst == "11001":
        rdict[reg] = rdict[reg] << imm
    elif inst == "10010":
        rdict[reg] = imm

def execute_typeC(Instruction):
    # reset flags


    reg1 = Instruction[10:13]
    reg2 = Instruction[13:16]
    inst = Instruction[0:5]
    if inst == "10011":
        if reg1 == "111":
            rdict[reg2] = int(''.join(rdict["111"]), 2)
        else:
            rdict[reg2] = rdict[reg1]
        
    rdict["111"] = ['0','0','0','0']

    if inst == "10111":
        rdict["000"] = int(rdict[reg1] / rdict[reg2])
        rdict["001"] = rdict[reg1] % rdict[reg2]
    elif inst == "11101":
        rdict[reg2] = ~rdict[reg1]
    elif inst == "11110":
        if rdict[reg1] < rdict[reg2]:
            rdict["111"][-3] = '1'
        elif rdict[reg1] > rdict[reg2]:
            rdict["111"][-2] = '1'
        elif rdict[reg1] == rdict[reg2]:
            rdict["111"][-1] = '1'

def ExecuteInstruction(Instruction):
    global PC
    global halted
    if Instruction[0:5] in ["10000","10001","10110","11010" ,"11011","11100"]:
        execute_typeA(Instruction)
    elif Instruction[0:5] in ["11000","11001", "10010"]:
        execute_typeB(Instruction)
    elif Instruction[0:5] in ["10011","10111", "11101", "11110"]:
        execute_typeC(Instruction)
    elif Instruction[0:5] in ["10101", "10100"]:
        # TypeD
        # store
        if Instruction[0:5] == "10101":
            Memory[convertToDecimal(Instruction[8:16])] = '0'*(16-len(bin(rdict[Instruction[5:8]])[2:])) + bin(rdict[Instruction[5:8]])[2:]
        # load
        elif Instruction[0:5] == "10100":
            rdict[Instruction[5:8]] = convertToDecimal(Memory[convertToDecimal(Instruction[8:16])])
        # rdict["111"] = ['0','0','0','0']

    elif Instruction[0:5] in ["01111", "01101", "11111", "01100"]:
        # TypeE
        # je
        if Instruction[0:5] == "01111":
            if rdict["111"][-1] == '1':
                PC = convertToDecimal(Instruction[8:16]) - 1
        # jgt
        elif Instruction[0:5] == "01101":
            if rdict["111"][-2] == '1':
                PC = convertToDecimal(Instruction[8:16]) - 1
        # jlt
        elif Instruction[0:5] == "01100":
            if rdict["111"][-3] == '1':
                PC = convertToDecimal(Instruction[8:16]) - 1
        # jmp
        elif Instruction[0:5] == "11111":
            PC = convertToDecimal(Instruction[8:16]) - 1
        # rdict["111"] = ['0','0','0','0']

    elif Instruction[0:5] == "01010":
        halted = True
    else:
        pass
    PC = PC + 1


while (not halted):
    Inst = Memory[PC]
    sys.stdout.write('0'*(8-len(bin(PC)[2:])) + bin(PC)[2:] + ' ')
    ExecuteInstruction(Inst)


    for i in rdict:
        if i != "111":
            sys.stdout.write('0'*(16-len(bin(rdict[i])[2:])) + bin(rdict[i])[2:] + ' ')
        else :
            sys.stdout.write("0"*12 + ''.join(rdict[i]) + '\n')


for i in range(256):
    sys.stdout.write(Memory[i]+'\n')


# initialize(MEM); // Load memory from stdin
# PC = 0; // Start from the first instruction
# halted = false;
# while(not halted)
# {
# Instruction = MEM.getData(PC); // Get current instruction
# halted, new_PC = EE.execute(Instruction); // Update RF compute new_PC
# PC.dump(); // Print PC
# RF.dump(); // Print RF state
# PC.update(new_PC); // Update PC
# }
# MEM.dump() // Print memory state
