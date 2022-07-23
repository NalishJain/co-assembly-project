import sys

rdict = { "000" : 0
        , "001": 0
        , "010": 0
        , "011": 0
        , "100": 0
        , "101": 0
        , "110": 0
        , "111": "0000"
}

assembly_input = sys.stdin.read().split('\n')
init_lst = [i.split() for i in assembly_input]
Memory = []

for i in range(256):
    Memory.append("0000000000000000")

for i in range(len(init_lst)):
    Memory[i] = init_lst[i]

PC = 0
halted = False


def execute_typeA(Instruction):

    rdict["111"] = "0000"

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
    rdict["111"] = "0000"

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
    rdict["111"] = "0000"

    reg1 = Instruction[10:13]
    reg2 = Instruction[13:16]
    inst = Instruction[0:5]
    if inst == "10011":
        rdict[reg2] = rdict[reg1]
    elif inst == "10111":
        rdict["000"] = int(rdict[reg1] / rdict[reg2])
        rdict["001"] = rdict[reg1] % rdict[reg2]
    elif inst == "11101":
        rdict[reg2] = ~rdict[reg1]
    elif inst == "11110":
        if rdict[reg1] < rdict[reg2]:
            rdict["111"][-3] = 1
        elif rdict[reg1] > rdict[reg2]:
            rdict["111"][-2] = 1
        elif rdict[reg1] == rdict[reg2]:
            rdict["111"][-1] = 1

def ExecuteInstruction(Instruction):
    if Instruction[0:5] in ["10000","10001","10110","11010" ,"11011","11100"]:
        execute_typeA(Instruction)
    elif Instruction[0:5] in ["11000","11001", "10010"]:
        execute_typeB(Instruction)
    elif Instruction[0:5] in ["10011","10111", "11101", "11110"]:
        execute_typeC(Instruction)
    elif Instruction[0:5] in ["10101", "10100"]:
        # TypeD
    elif Instruction[0:5] in ["01111", "01101", "11111", "01100"]:
        # TypeE
    elif Instruction[0:5] == "01010":
        global halted = True
    else:


while (not halted):
    Inst = Memory[PC]
    sys.stdout.write('0'*(8-len(bin(PC)[2:])) + bin(PC)[2:] + ' ')
    PC = ExecuteInstruction(Inst)


    for i in rdict:
        if i != "111":
            sys.stdout.write('0'*(16-len(bin(rdict[i])[2:])) + bin(rdict[i])[2:] + ' ')
        else :
            sys.stdout.write("0"*12 + rdict[i] + '\n')

