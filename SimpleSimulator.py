import sys
# Flag variables

FlagV = 0
FlagL = 0
FlagG = 0
FlagE = 0


rdict = {
            "000": 0,
            "001": 0,
            "010": 0,
            "011": 0,
            "100": 0,
            "101": 0,
            "110": 0,
            "111": 0
        }

assembly_input = sys.stdin.read().split('\n')
init_lst = [i for i in assembly_input]
Memory = []

for i in range(256):
    Memory.append("0000000000000000")

for i in range(len(init_lst)):
    Memory[i] = init_lst[i]

PC = 0
halted = False

def convertToDecimal(binary):
    total = 0
    power = 0
    while binary != '':
        total += int(binary[len(binary)-1]) * power
        power += 1
        binary = binary[:len(binary)-1]
    return total

def ExecuteInstruction(Instruction):
    global PC
    global halted
    if Instruction[0:5] in ["10000","10001","10110","11010" ,"11011","11100"]:
        # TypeA
    elif Instruction[0:5] in ["11000", "11001"]:
        # TypeB
    elif Instruction[0:5] in ["10111", "11101", "11110"]:
        # TypeC
    elif Instruction[0:5] in ["10101", "10100"]:
        # TypeD
        # store
        if Instruction[0:5] == "10101":
            Memory[convertToDecimal(Instruction[8:16])] = rdict[Instruction[5:8]]
        # load
        elif Instruction[0:5] == "10100":
            rdict[Instruction[5:8]] = Memory[convertToDecimal(Instruction[8:16])]

    elif Instruction[0:5] in ["01111", "01101", "11111", "01100"]
        # TypeE
        # je
        if Instruction[0:5] == "01111":
            if FlagE = 1:
                PC = convertToDecimal(Instruction[8:16]) - 1
        # jgt
        elif Instruction[0:5] == "01101":
            if FlagG = 1:
                PC = convertToDecimal(Instruction[8:16]) - 1
        # jlt
        elif Instruction[0:5] == "01100":
            if FlagL = 1:
                PC = convertToDecimal(Instruction[8:16]) - 1
        # jmp
        elif Instruction[0:5] == "11111":
            PC = convertToDecimal(Instruction[8:16]) - 1

    elif Instruction[0:5] == "01010":
        # TypeF
    else:


while (not halted):
    Inst = Memory[PC]
    sys.stdout.write(str(PC)+' ')
    halted, PC = ExecuteInstruction(Inst)
    for i in rdict.keys():
        sys.stdout.write(rdict[i]+' ')
    sys.stdout.write('\n')

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
