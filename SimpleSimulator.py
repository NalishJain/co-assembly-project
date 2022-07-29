import sys
# import matplotlib.pyplot as plt
# from matplotlib.ticker import FuncFormatter
# import numpy as np
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
init_lst = [i for i in assembly_input if i != '']
Memory = []
memory_access_trace = []
timestep = 1

for i in range(256):
    Memory.append("0000000000000000")

for i in range(len(init_lst)):
    Memory[i] = init_lst[i]

PC = 0
halted = False


def convertToDecimal(binary):
    d = int(binary,2)
    return d

def BinaryfloatToDecimal(exp, matissa):
    mand = (2**exp)*( 1 + int(matissa[0])*(2**(-1)) + int(matissa[1])*(2**(-2)) + int(matissa[2])*(2**(-3)) + int(matissa[3])*(2**(-4)) + int(matissa[4])*(2**(-5)))
    return mand

def DecimalToBinary(num):
    exp = 0
    while num/2>1:
        num = num/2
        exp += 1
    while num*2 < 1:
        num = num*2
        exp -= 1

    exp_bin = bin(exp)[2:]

    decimal = float(str(num)[1:])
    mantissa = ""
    while len(mantissa)<5 and decimal != 0:
        mantissa += str(int((decimal*2) // 1))
        decimal = (decimal*2) % 1

    if len(exp_bin) > 3 or len(mantissa)>5 or decimal != 0:
        sys.stdout.write(f'Error at line {line_num}: Cannot represent given float in 8-bits\n')
        sys.exit()
    immediate = '0' * (3-len(exp_bin)) + exp_bin + mantissa + '0' * (5-len(mantissa))
    return immediate

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
        r1b = ('0'*(16-len(bin(rdict[Instruction[7:10]])[2:])) + bin(rdict[Instruction[7:10]])[2:])
        r1c = ('0'*(16-len(bin(rdict[Instruction[10:13]])[2:])) + bin(rdict[Instruction[10:13]])[2:])
        r1a = ''

        for i in range(0,16):
            if (r1b[i] == '0' and r1c[i] == '0') or  (r1b[i] == '1' and r1c[i] == '1'):
                r1a = r1a + '0'
            else:
                r1a = r1a + '1'

        resA = convertToDecimal(r1a)
        rdict[Instruction[13:16]] = resA

    elif  Instruction[0:5] == "11011":
        r1b = ('0'*(16-len(bin(rdict[Instruction[7:10]])[2:])) + bin(rdict[Instruction[7:10]])[2:])
        r1c = ('0'*(16-len(bin(rdict[Instruction[10:13]])[2:])) + bin(rdict[Instruction[10:13]])[2:])
        r1a = ''

        for i in range(0,16):
            if r1b[i] == '0' and r1c[i] == '0':
                r1a = r1a + '0'
            else:
                r1a = r1a + '1'

        resA = convertToDecimal(r1a)
        rdict[Instruction[13:16]] = resA

    elif Instruction[0:5] == "11100":
        r1b = ('0'*(16-len(bin(rdict[Instruction[7:10]])[2:])) + bin(rdict[Instruction[7:10]])[2:])
        r1c = ('0'*(16-len(bin(rdict[Instruction[10:13]])[2:])) + bin(rdict[Instruction[10:13]])[2:])
        r1a = ''
        for i in range(0,16):
            if r1b[i] == '1' and r1c[i] == '1':
                r1a = r1a + '1'
            else:
                r1a = r1a + '0'

        resA = convertToDecimal(r1a)
        rdict[Instruction[13:16]] = resA

    elif  Instruction[0:5] == "00000":
        resB = ('0'*(16-len(bin(rdict[Instruction[7:10]])[2:])) + bin(rdict[Instruction[7:10]])[2:])[8:16]
        resC = ('0'*(16-len(bin(rdict[Instruction[10:13]])[2:])) + bin(rdict[Instruction[10:13]])[2:])[8:16]
        resBexp = convertToDecimal(resB[0:3])
        resBmantissa = resB[3:8]
        resCexp = convertToDecimal(resC[0:3])
        resCmantissa = resC[3:8]
        resBfloat = BinaryfloatToDecimal(resBexp, resBmantissa)
        resCfloat = BinaryfloatToDecimal(resCexp, resCmantissa)
        resAfloat = resBfloat + resCfloat
        if (resAfloat <= 252.0):
            resAI = DecimalToBinary(resAfloat)
            rdict[Instruction[13:16]] = convertToDecimal("00000000" + resAI)
            # ConversionFunction

        else:
            rdict["111"][0] = '1'
            rdict[Instruction[13:16]] = convertToDecimal("0000000011111111")

    elif  Instruction[0:5] == "00001":

        resB = ('0'*(16-len(bin(rdict[Instruction[7:10]])[2:])) + bin(rdict[Instruction[7:10]])[2:])[8:16]
        resC = ('0'*(16-len(bin(rdict[Instruction[10:13]])[2:])) + bin(rdict[Instruction[10:13]])[2:])[8:16]

        resBexp = convertToDecimal(resB[0:3])
        resBmantissa = resB[3:8]
        resCexp = convertToDecimal(resC[0:3])
        resCmantissa = resC[3:8]

        resBfloat = BinaryfloatToDecimal(resBexp, resBmantissa)
        resCfloat = BinaryfloatToDecimal(resCexp, resCmantissa)

        resAfloat = resBfloat - resCfloat


        if (resAfloat >= 0):
             # ConversionFunction
            resAI = DecimalToBinary(resAfloat)
            rdict[Instruction[13:16]] = convertToDecimal("00000000" + resAI)

        else:
            rdict["111"][0] = '1'
            rdict[Instruction[13:16]] = convertToDecimal("0000000000000000")




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
    elif inst == "00010":
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
        binary = ''.join('1' if x == '0' else '0' for x in bin(rdict[reg1])[2:])
        binary = '1'*(16-len(binary)) + binary
        rdict[reg2] = int(binary, 2)
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
    if Instruction[0:5] in ["10000","10001", "10110","11010" ,"11011", "11100", "00000", "00001"]:
        execute_typeA(Instruction)
    elif Instruction[0:5] in ["11000","11001", "10010", "00010"]:
        execute_typeB(Instruction)
    elif Instruction[0:5] in ["10011","10111", "11101", "11110"]:
        execute_typeC(Instruction)
    elif Instruction[0:5] in ["10101", "10100"]:
        # TypeD
        # store
        if Instruction[0:5] == "10101":
            Memory[convertToDecimal(Instruction[8:16])] = '0'*(16-len(bin(rdict[Instruction[5:8]])[2:])) + bin(rdict[Instruction[5:8]])[2:]
            memory_access_trace.append(['0'*(16-len(bin(convertToDecimal(Instruction[8:16]))[2:])) + bin(convertToDecimal(Instruction[8:16]))[2:], timestep])
        # load
        elif Instruction[0:5] == "10100":
            rdict[Instruction[5:8]] = convertToDecimal(Memory[convertToDecimal(Instruction[8:16])])
            memory_access_trace.append(['0'*(16-len(bin(convertToDecimal(Instruction[8:16]))[2:])) + bin(convertToDecimal(Instruction[8:16]))[2:], timestep])

        rdict["111"] = ['0','0','0','0']

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
        rdict["111"] = ['0','0','0','0']

    elif Instruction[0:5] == "01010":
        halted = True
    else:
        pass
    PC = PC + 1


while (not halted):
    Inst = Memory[PC]
    memory_access_trace.append(['0'*(16-len(bin(PC)[2:])) + bin(PC)[2:], timestep])
    sys.stdout.write('0'*(8-len(bin(PC)[2:])) + bin(PC)[2:] + ' ')
    ExecuteInstruction(Inst)


    for i in rdict:
        if i != "111":
            sys.stdout.write('0'*(16-len(bin(rdict[i])[2:])) + bin(rdict[i])[2:] + ' ')
        else :
            sys.stdout.write("0"*12 + ''.join(rdict[i]) + '\n')

    timestep += 1

for i in range(256):
    sys.stdout.write(Memory[i]+'\n')


# plot_memory_trace = True
# if plot_memory_trace:
#     memory_access_trace = np.array(memory_access_trace)
#     fig, ax = plt.subplots()
#     ax.yaxis.set_major_formatter(FuncFormatter("{:08b}".format))
#     plt.xlabel('Cycle number')
#     plt.title('Memory trace: Address accessed vs cycle')
#     plt.scatter(memory_access_trace[:,1], memory_access_trace[:,0])
#     plt.show()

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
