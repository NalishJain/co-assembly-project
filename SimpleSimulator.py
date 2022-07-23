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
    if  Instruction[0:5] == "10000":
        resA = rdict[Instruction[7:10]] + rdict[Instruction[10:13]] 
        if resA < (2**16):
            rdict[Instruction[13:16]] = resA
        else:
            rdict["111"][0] = '1'
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

    elif  Instruction[0:5] == "11010":
        resA = (rdict[Instruction[7:10]])^(rdict[Instruction[10:13]]) 
        rdict[Instruction[13:16]] = resA

    elif  Instruction[0:5] == "11011":
        resA = (rdict[Instruction[7:10]])|(rdict[Instruction[10:13]]) 
        rdict[Instruction[13:16]] = resA

    else:
        resA = (rdict[Instruction[7:10]])&(rdict[Instruction[10:13]]) 
        rdict[Instruction[13:16]] = resA 


def ExecuteInstruction(Instruction):
    if Instruction[0:5] in ["10000","10001","10110","11010" ,"11011","11100"]:
        rdict["111"] = "0000"
        execute_typeA(Instruction)
    elif Instruction[0:5] in ["11000", "11001"]:
        # TypeB
    elif Instruction[0:5] in ["10111", "11101", "11110"]:
        # TypeC
    elif Instruction[0:5] in ["01111", "01101", "11111", "01100"]:
        # TypeD
    elif Instruction[0:5] in ["11000", "11001"]:
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

