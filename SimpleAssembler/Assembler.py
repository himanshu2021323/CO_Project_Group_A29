Opcode = {
    "add":"10000",
    "sub":"10001",
    "mov":"10010",
    "movr":"10100",
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
Register = {
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAG":"111"
}

with open("stdin.txt","r") as file1:
    Statements = file1.readlines()
with open("stdout.txt","w") as file2:
    file2.close()
    
def Error_Handling(Statements):
    with open("stdout.txt","a") as file2:
        error = 0
        for i in range(len(Statements)):
            line = str(Statements[i])
            line = line.split()
            if Statements[i]=='\n':
                pass
            elif((line[0] not in ["add","sub","mul","xor","or","and","mov","rs","ls","mov","div","not","cmp","ld","st","jmp","jlt","jgt","je","hlt"]) and line[0] != "var" and (line[0][-1] != ":")):
                x = f"line no:{str(i+1)} illegal opcode or typo error"
                print(f"line no:{str(i+1)} illegal opcode or typo error")
                file2.write("\n")
                file2.write(x)
                error = 1
                break
            elif(line[0] in (["add","sub","mul","xor","or","and"] or ["mov","rs","ls"] or ["ld","st"])) and (line[1] not in ["R0","R1","R2","R3","R4","R5","R6","FLAG"]): 
                print(f"line no:{str(i+1)} typo in register name1")
                x = f"line no:{str(i+1)} typo in register name"
                error = 1
                file2.write("\n")
                file2.write(x)
                break
            elif(line[0] in ["mov","div","not","cmp"] ) and (line[2][0] == "$") and  ((line[1] not in ["R0","R1","R2","R3","R4","R5","R6","FLAG"])):
                print(f"line no:{str(i+1)} typo in register name2")
                x = f"line no:{str(i+1)} typo in register name"
                file2.write("\n")
                file2.write(x)
                error = 1
                break 
            elif(line[0] in ["ld","st"] ) and ((line[1] not in ["R0","R1","R2","R3","R4","R5","R6","FLAG"])):
                print(f"line no:{str(i+1)} typo in register name3")
                x = f"line no:{str(i+1)} typo in register name"
                file2.write("\n")
                file2.write(x)
                error = 1
                break 
            elif(line[0] in ["add","sub","mul","xor","or","and"] ) and ((line[2] not in ["R0","R1","R2","R3","R4","R5","R6","FLAG"]) or (line[3] not in ["R0","R1","R2","R3","R4","R5","R6","FLAG"])):
                print(f"line no:{str(i+1)} typo in register name4")
                x = f"line no:{str(i+1)} typo in register name"
                file2.write("\n")
                file2.write(x)
                error = 1
                break 
            elif(line[0] in ["mov","rs","ls"]) :
                s1 = str(line[2][1:])
                s1 = int(s1)
                if(s1 <= 0 or s1 >= 255):
                    print(f"line no:{str(i+1)} illegal immediate value")
                    x = f"line no:{str(i+1)} illegal immediate value"
                    error = 1
                    file2.write("\n")
                    file2.write(x)
                    break
            elif((line[0] in ["hlt"]) and i != (len(Statements)-1)):
                print(f"line no:{str(i+1)} hlt used before last 1")
                x = f"line no:{str(i+1)} hlt used before last 1"
                file2.write("\n")
                file2.write(x)
                error = 1
                break   
            elif((i == (len(Statements)-1)) and line[0] != "hlt"):
                print(f"line no:{str(i+1)} hlt not present at last")
                x = f"line no:{str(i+1)} hlt not present at last"
                file2.write("\n")
                file2.write(x)
                error = 1
                break
            elif((line[0] in ["ld","st"]) or (line[0] in ["jmp","jlt","jgt","je"])):
                s1="var"+" "+line[2]
                if (s1 in Statements):
                    print(f"line no:{str(i+1)} var not defined")
                    x = f"line no:{str(i+1)} var not defined"
                    file2.write("\n")
                    file2.write(x)
                    error = 1
                    break
            elif((line[0] in ["add","sub","mul","xor","or","and"]) and ((line[1] or line[2] or line[3]) == "FLAG") ):
                print(f"line no:{str(i+1)} illegal use of flag ")
                x = f"line no:{str(i+1)} illegal use of flag "
                file2.write("\n")
                file2.write(x)
                error = 1
                break
            elif(line[0] in ["mov","rs","ls"]) and ((line[1] or line[2]) == "FLAG"):
                print(f"line no:{str(i+1)} illegal use of flag ")
                x = f"line no:{str(i+1)} illegal use of flag "
                file2.write("\n")
                file2.write(x)
                error = 1
                break
            elif(line[0] in ["mov","div","not","cmp"]) and (line[1] != "mov") and (line[2] or line[1] == "FLAG"):
                print(f"line no:{str(i+1)} illegal use of flag ")
                x = f"line no:{str(i+1)} illegal use of flag "
                file2.write("\n")
                file2.write(x)
                error = 1
                break
            elif((line[0] in ["ld","st"]) and (line[1] or line[2]) == "FLAG"):
                print(f"line no:{str(i+1)} illegal use of flag ")
                x = f"line no:{str(i+1)} illegal use of flag "
                file2.write("\n")
                file2.write(x)
                error = 1
                break
            elif((line[0] in ["jmp","jlt","jgt","je"]) and (line[1] ) == "FLAG"):
                print(f"line no:{str(i+1)} illegal use of flag ")
                x = f"line no:{str(i+1)} illegal use of flag "
                file2.write("\n")
                file2.write(x)
                error = 1
                break
    return error        

def counter(Statements, mem_addr):
    count = 0
    for i in range(len(Statements)):
        line1 = str(Statements[i])
        line1 = line1.split()
        if Statements[i] == '\n':
            pass
        elif line1[0] in ["add","sub","mul","xor","or","and","mov","rs","ls","mov","div","not","cmp","ld","st","jmp","jlt","jgt","je","hlt"]:
            count += 1
    for i in range(len(Statements)):
        line1 = str(Statements[i])
        line1 = line1.split()
        if Statements[i] == '\n':
            pass
        elif (line1[0] == "var") and (line1[1] != mem_addr):
            count += 1
        elif (line1[0] == "var") and (line1[1] == mem_addr) :
            break
    return count

def Encoding(Statements):
    with open("stdout.txt","a") as file2:
        for i in range(len(Statements)):
            line = str(Statements[i])
            line = line.split()
            if Statements[i] == '\n':
                pass
            elif(line[0] in ["add","sub","mul","xor","or","and"]):
                typeA = Opcode[line[0]] + "0"*2 + Register[line[1]] + Register[line[2]] + Register[line[3]]
                print(typeA)
                file2.write("\n")
                file2.write(typeA)
            elif(line[0] in ["mov","rs","ls"] and line[2][0] == "$"):
                line1 = str(line[2][1:])
                line2 = len(line1)
                line1 = int(line1)
                line3 = bin(line1)[2:]
                line3 = str(line3)
                line4 = len(line3)
                typeB = Opcode[line[0]] + Register[line[1]] + "0"*(8-len(line3)) + line3
                print(typeB)
                file2.write("\n")
                file2.write(typeB)
            elif(line[0] in ["mov","div","not","cmp"] and line[2][0] != "$"):
                typeC = Opcode[line[0]] + "0"*5 + Register[line[1]] + Register[line[2]]
                print(typeC)
                file2.write("\n")
                file2.write(typeC)
            elif(line[0] in ["ld","st"]):
                mem_addr = line[2]   
                mem_addr1 = counter(Statements,mem_addr)
                line3 = bin(mem_addr1)[2:]
                typeD = Opcode[line[0]] + Register[line[1]] + "0"*(8-len(line3)) + line3
                print(typeD)
                file2.write("\n")
                file2.write(typeD)
            elif(line[0] in ["jmp","jlt","jgt","je"]):
                mem_addr = line[2]   
                mem_addr1 = counter(Statements,mem_addr)
                line3 = bin(mem_addr1)[2:]
                typeE = Opcode[line[0]] + "0"*3 + "0"*(8-len(line3)) + line3
                print(typeE)
                file2.write("\n")
                file2.write(typeE)
            elif(line[0] in ["hlt"]):
                typeF = Opcode[line[0]] + "0"*11
                print(typeF)
                file2.write("\n")
                file2.write(typeF)
            elif(line[0][len(line[0])-1] == ":"):
                pass 

if(Error_Handling(Statements)!=1):
    Encoding(Statements)
