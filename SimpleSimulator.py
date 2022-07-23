import sys

rdict = { "000" : 0
        , "001": 0
        , "010": 0
        , "011": 0
        , "100": 0
        , "101": 0
        , "110": 0
        , "111": 0
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

def ExecuteInstruction(Instruction):
    if Instruction[0:5] in ["10000","10001","10110","11010" ,"11011","11100"]:
        # TypeA
    elif Instruction[0:5] in ["11000", "11001"]:
        # TypeB
    elif Instruction[0:5] in ["10111", "11101", "11110"]:
        # TypeC
    elif Instruction[0:5] in ["01111", "01101", "11111", "01100"]:
        # TypeD
    elif Instruction[0:5] in ["11000", "11001"]:
        # TypeE
    elif Instruction[0:5] == "01010":
        # TypeF
    else:
        

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