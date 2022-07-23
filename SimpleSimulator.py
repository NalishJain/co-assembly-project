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
    # TODO: Reset FLAGS if inst does not affect FLAGS reg, I have handled type B,C

    if Instruction[0:5] in ["10000","10001","10110","11010" ,"11011","11100"]:
        # TypeA
        rdict["111"] = "0000"
    elif Instruction[0:5] in ["11000", "11001"]:
        execute_typeB(Instruction)
    elif Instruction[0:5] in ["10111", "11101", "11110"]:
        execute_typeC(Instruction)
    elif Instruction[0:5] in ["01111", "01101", "11111", "01100"]:
        # TypeD
    elif Instruction[0:5] in ["11000", "11001"]:
        # TypeE
    elif Instruction[0:5] == "01010":
        # TypeF
    else:
    
    if 

while (not halted):
    Inst = Memory[PC]
    print(PC, end = " ")
    halted, PC = ExecuteInstruction(Inst)






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