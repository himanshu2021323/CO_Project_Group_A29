from sys import stdin

registers = {   "000": "0"*16,
                "001": "0"*16,
                "010": "0"*16,
                "011": "0"*16,
                "100": "0"*16,
                "101": "0"*16,
                "110": "0"*16,
                "111": ["0", "0", "0", "0"]
            }

main_List = []
memory_List = []
variable_List = {}
halt = False
halt_Flag = False

for Input in stdin:
    if(Input != ""):
        Input = Input.strip()
        if(Input == ""):
            continue
        main_List.append(Input)
    else:
        break


def add(r1, r2, r3):
    reg1 = registers[r1]
    reg2 = registers[r2]
    reg3 = registers[r3]
    overFlow = False
    re1 = int(reg1, 2)
    re2 = int(reg2, 2)
    re3 = int(reg3, 2)

    re3 = re1 + re2

    if(re3 < 0):
        re3 = 0
        registers["111"][0] = "1"
    elif(re3 > 65535):
        registers["111"][0] = "1"
        overFlow = True

    binary = bin(re3)[2:]

    if(overFlow):
        takeOverFlow = len(binary)-16
        binary = binary[takeOverFlow:]
    else:
        registers["111"]= ["0", "0", "0", "0"]
    registers[r3] = binary.zfill(16)


def sub(r1, r2, r3):
    reg1 = registers[r1]
    reg2 = registers[r2]
    reg3 = registers[r3]
    overFlow = False
    re1 = int(reg1, 2)
    re2 = int(reg2, 2)
    re3 = int(reg3, 2)

    re3 = re1 - re2

    if(re3 < 0):
        re3 = 0
        registers["111"][0] = "1"
        overFlow = True
    elif(re3 >= 65535):
        registers["111"][0] = "1"
        overFlow = True

    binary = bin(re3)[2:]

    if(overFlow):
        takeOverFlow = len(binary)-16
        binary = binary[takeOverFlow:]
    else:
        registers["111"]= ["0", "0", "0", "0"]
    registers[r3] = binary.zfill(16)


def mul(r1, r2, r3):
    reg1 = registers[r1]
    reg2 = registers[r2]
    reg3 = registers[r3]
    overFlow = False
    re1 = int(reg1, 2)
    re2 = int(reg2, 2)
    re3 = int(reg3, 2)

    re3 = re1 * re2

    if(re3 < 0):
        re3 = 0
        registers["111"][0] = "1"
    elif(re3 > 65535):
        registers["111"][0] = "1"
        overFlow = True

    binary = bin(re3)[2:]

    if(overFlow):
        takeOverFlow = len(binary)-16
        binary = binary[takeOverFlow:]
        registers["111"]= ["1", "0", "0", "0"]
    else:
        registers["111"]= ["0", "0", "0", "0"]

    registers[r3] = binary.zfill(16)


def div(r3, r4):

    reg3 = registers[r3]
    reg4 = registers[r4]
    re3 = int(reg3, 2)
    re4 = int(reg4, 2)
    re0 = re3//re4
    re1 = re3 % re4
    binary0 = bin(re0)[2:]
    binary1 = bin(re1)[2:]

    registers["000"] = binary0.zfill(16)
    registers["001"] = binary1.zfill(16)
    registers["111"]= ["0", "0", "0", "0"]


def movimm(reg1, imm):
    r1 = imm
    registers[reg1] = r1.zfill(16)
    registers["111"]= ["0", "0", "0", "0"]


def movreg(reg1, reg2):
    if(reg2 == "111"):
        flag_Register = "".join(registers["111"]).zfill(16)
        registers[reg1] = flag_Register
    else:
        r1= registers[reg2]
        registers[reg1] = r1
    registers["111"]= ["0", "0", "0", "0"]


def ld(reg1, memory):
    try:
        r1 = variable_List[memory]
    except:
        r1="0000000000000000"
    registers[reg1] = r1
    registers["111"]= ["0", "0", "0", "0"]


def st(reg1, memory):
    variable_List[memory] = registers[reg1]
    registers["111"]= ["0", "0", "0", "0"]


def right_shift(reg1, imm):
    n = int(imm, 2)
    re1 = int(registers[reg1], 2)

    re1 = re1 >> n
    
    binary1 = bin(re1)[2:]
    registers[reg1] = binary1.zfill(16)
    registers["111"]= ["0", "0", "0", "0"]


def left_shift(reg1, imm):
    n = int(imm, 2)
    re1 = int(registers[reg1], 2)

    re1 = re1 << n
    
    binary1 = bin(re1)[2:]
    registers[reg1] = binary1.zfill(16)
    registers["111"]= ["0", "0", "0", "0"]


def xor(reg1, reg2, reg3):
    re1 = int(registers[reg1], 2)
    re2 = int(registers[reg2], 2)
    re3 = int(registers[reg3], 2)

    re3 = re1 ^ re2

    binary = bin(re3)[2:]
    registers[reg3] = binary.zfill(16)
    registers["111"]= ["0", "0", "0", "0"]


def oor(reg1, reg2, reg3):
    re1 = int(registers[reg1], 2)
    re2 = int(registers[reg2], 2)
    re3 = int(registers[reg3], 2)

    re3 = re1 | re2

    binary = bin(re3)[2:]
    registers[reg3] = binary.zfill(16)
    registers["111"]= ["0", "0", "0", "0"]


def aand(reg1, reg2, reg3):
    re1 = int(registers[reg1], 2)
    re2 = int(registers[reg2], 2)
    re3 = int(registers[reg3], 2)

    re3 = re1 & re2

    binary = bin(re3)[2:]
    registers[reg3] = binary.zfill(16)
    registers["111"]= ["0", "0", "0", "0"]


def invert(reg1, reg2):
    temp = ""
    for i in registers[reg2]:
        if(i == "0"):
            temp = temp+"1"
        else:
            temp = temp + "0"
    registers[reg1] = temp.zfill(16)
    registers["111"]= ["0", "0", "0", "0"]


def cmp(r1, r2):
    reg1= registers[r1]
    reg2 = registers[r2]
    re1 = int(reg1, 2)
    re2 = int(reg2, 2)
    if(re1 == re2):
        registers["111"][3] = "1"
    elif(re1>re2):
        registers["111"][2] = "1"
    elif(re1<re2):
        registers["111"][1] = "1"


def uncjmp():
    mem_Address = code[8:16]
    registers["111"]= ["0", "0", "0", "0"]
    return int(mem_Address, 2)


def jlt():
    mem_Address = code[8:16]
    registers["111"]= ["0", "0", "0", "0"]
    return int(mem_Address, 2)


def jgt():
    mem_Address = code[8:16]
    registers["111"]= ["0", "0", "0", "0"]
    return int(mem_Address, 2)


def je():
    mem_Address = code[8:16]
    registers["111"]= ["0", "0", "0", "0"]
    return int(mem_Address, 2)


def hlt():
    registers["111"]= ["0", "0", "0", "0"]
    halt = True


i = 0
while i <= (len(main_List)-1):
    programCounter = bin(i)[2:].zfill(8)
    code = main_List[i]

    opCodes = code[0:5]

    if opCodes == "10000":
        reg1 = code[7:10]
        reg2 = code[10:13]
        reg3 = code[13:]
        
        add(reg1, reg2, reg3)
        i += 1

    elif opCodes == "10001":
        reg1 = code[7:10]
        reg2 = code[10:13]
        reg3 = code[13:]

        sub(reg1, reg2, reg3)
        i += 1

    elif opCodes == "10010":
        reg1 = code[5:8]
        imm = "00000000" + code[8:]
        
        movimm(reg1, imm)
        i += 1

    elif opCodes == "10011":
        reg1 = code[10:13]
        reg2 = code[13:]

        movreg(reg1, reg2)
        i += 1

    elif opCodes == "10100":
        reg1 = code[5:8]
        mem_Variable = code[8:]
        
        ld(reg1, mem_Variable)
        i += 1

    elif opCodes == "10101":
        reg1 = code[5:8]
        mem_Variable = code[8:]
        
        st(reg1, mem_Variable)
        i += 1

    elif opCodes == "10110":
        reg1 = code[7:10]
        reg2 = code[10:13]
        reg3 = code[13:]

        mul(reg1, reg2, reg3)

        i += 1

    elif opCodes == "10111":
        reg1 = code[10:13]
        reg2 = code[13:16]

        div(reg1, reg2)

        i += 1

    elif opCodes == "11000":
        reg1 = code[5:8]
        imm = "0"*8 + code[8:]

        right_shift(reg1, imm)
        i += 1

    elif opCodes == "11001":
        reg1 = code[5:8]
        imm = "0"*8 + code[8:]

        left_shift(reg1, imm)
        i += 1

    elif opCodes == "11010":
        reg1 = code[7:10]
        reg2 = code[10:13]
        reg3 = code[13:]

        xor(reg1, reg2, reg3)
        i += 1

    elif opCodes == "11011":
        reg1 = code[7:10]
        reg2 = code[10:13]
        reg3 = code[13:]

        oor(reg1, reg2, reg3)
        i += 1

    elif opCodes == "11100":
        reg1 = code[7:10]
        reg2 = code[10:13]
        reg3 = code[13:]

        aand(reg1, reg2, reg3)
        i += 1

    elif opCodes == "11101":
        reg1 = code[10:13]
        reg2 = code[13:]

        invert(reg1, reg2)
        i += 1

    elif opCodes == "11110":
        reg1 = code[10:13]
        reg2 = code[13:]

        cmp(reg1, reg2)
        i += 1

    elif opCodes == "11111":
        i = uncjmp()

    elif opCodes == "01100":

        if registers["111"][1] == "1":
            i = jlt()
        else:
            registers["111"]= ["0", "0", "0", "0"]
            i += 1

    elif opCodes == "01101":
        if registers["111"][2] == "1":
            i = jgt()

        else:
            registers["111"]= ["0", "0", "0", "0"]
            i += 1

    elif opCodes == "01111":
        if registers["111"][3] == "1":
            i = je()

        else:
            registers["111"]= ["0", "0", "0", "0"]
            i += 1

    elif opCodes == "01010":
        registers["111"]= ["0", "0", "0", "0"]
        halt_Flag = True
        i += 1


    # printing part
    PRINT = "".join(registers["111"]).zfill(16)
    EE = programCounter+" " + registers["000"] + " " + registers["001"] + " " + registers["010"] + " " + registers["011"] + " " + registers["100"] + " " + registers["101"] + " " + registers["110"] + " " + PRINT
    memory_List.append(EE)
    if(halt_Flag):
        break

# memoryDump
dmpCount = 0
for i in main_List:
    memory_List.append(i)
    dmpCount = dmpCount + 1
Items = variable_List.items()
variable_List = sorted(Items)

if(len(variable_List) > 0):
    for i in variable_List:
        memory_List.append(i[1])
        dmpCount += 1

extLines = 256 - dmpCount
for i in range(extLines):
    memory_List.append("0000000000000000")

for i in memory_List:
    print(i)
