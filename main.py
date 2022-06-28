
#Global Constants
MAX_LINES = 256
REG_SIZE = 3
MEM_SIZE = 8
OPCODE_SIZE = 5
IMM_SIZE = 8

rdict = {"R0" : "000",
        "R1" : "001", 
        "R2" : "010", 
        "R3" : "011", 
        "R4" : "100", 
        "R5" : "101", 
        "R6" : "110", 
        "FLAGS" : "110"}

def typeA(lst):
    s = get_opcode[lst[0]] + "00" + get_reg[lst[1]] + get_reg[lst[2]] + get_reg[lst[3]]
    return s

def typeF(lst):
    s = get_opcode[lst[0]] + "00000000000"
    return s


if (get_opcode[lst[0]] in ["10000","10001","10110","11010" ,"11011","11100"]):
    s = typeA(lst)
elif (get_opcode[lst[0]] in ["11001", "10010"]):
    s = typeB(lst)
elif (get_opcode[lst[0]] in ["10011", "10111", "11101", "11110"]):
    s = typeC(lst)
elif (get_opcode[lst[0]] in ["10101", "10100"]):
    s = typeD(lst)
elif (get_opcode[lst[0]] in ["01111", "01101", "11111", "01100"]):
    s = typeE(lst)
else:
    s = typeF(lst)            

#----EOF----
