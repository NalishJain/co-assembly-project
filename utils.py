from pickletools import opcodes
import errors

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
        "R6" : "110"}

opCode = {
        "add":"10000",
        "sub":"10001",
        "movi":"10010",
        "movr":"10011",
        "ld":"10100",
        "st":"10101",
        "mul":"10110",
        "div":"10111",
        "rs":"11000",
        "ls":"11001",
        "xor":"11010",
        "or":"11011",
        "and":"11100",
        "not":"11101",
        "cmp":"11110",
        "jmp":"11111",
        "jlt":"01100",
        "jgt":"01101",
        "je":"01111",
        "hlt":"01010"
        }


def get_reg(reg, line_num):
    errors.check_reg(reg, rdict, line_num)
    return rdict[reg]


def get_opcode(ins, line_num):
    errors.check_opcode(ins, opCode, line_num)
    return opCode[ins]

def missing_hlt(lst):
    if lst[-1][0] != "hlt":
        raise Exception("Halt instruction not present at the end")

def hlt_not_at_end(lst):
    for i in range(len(lst) - 1):
        if lst[i] == []:
            continue
        if lst[i][0] == "hlt":
            raise Exception("Halt instruction should be the last instruction only")
