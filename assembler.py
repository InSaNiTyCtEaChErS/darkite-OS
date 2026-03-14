opcodes = "add awc sub swc nand and rol ror jmp bra be bne bl bg bb ba ioio call ret push pull cmp llp lup ".split()
register_remap = []
macros = []
map_ = []
constants = []

def getopc(opc):    #get the opcode of a operation based on the first token
    global opcodes
    opc = opc.strip()
    if opc[-1] == "i":
        opc = opc[:-1]
    return(("000000"+str(bin(opcodes.index(opc))[2:]))[-5:])

def getreg(reg): #get a register value given either the register or it's name
    global register_remap
    global map_
    global constants
    if reg in constants:
        return(constants[constants.index(reg)+1])
    elif reg in map_:
        return("00000"+str(bin(int(register_remap[map_.index(reg)][1:]))[2:]))[-5:] + "0000000000000000"
    elif reg.isdigit():
        return("00000"+bin(int(reg))[2:])[-5:]+"00000000000000000"
    else:
        return("00000"+str(bin(int(reg[1:]))[2:]))[-5:] + "0000000000000000"
    
def z_arg_enc(line,i):
    return("00000000000"+getopc(line)+i+"000000000000000")

def m_arg_enc_b(line,i):   #encode all operations with one argument (source)
    line = line.split()
    return(getreg(line[1])[5:16]+getopc(line[0])+i+"00000"+getreg(line[1])[0:5]+"00000")

def m_arg_enc_c(line):   #encode all operations with one argument (dest)
    line = line.split()
    return("00000000000"+getopc(line[0])+"0"+"0000000000"+getreg(line[1])[0:5])

def d_arg_enc_c(line,i): #encode all operations with two arguments
    line = line.split()
    return(getreg(line[2])[5:16]+getopc(line[0])+i+getreg(line[1])[0:5]+getreg(line[2])[0:5]+"00000")

def t_arg_enc(line,i): #encode all operations with three arguments
    line = line.split()
    return(getreg(line[2])[5:16]+getopc(line[0])+i+getreg(line[1])[0:5]+getreg(line[2])[0:5]+getreg(line[3])[0:5])

def enc(arg): #encode a line of code
    if not len(arg) == 0:
        arg = arg.replace(","," ")
        i = "0"
        out = ""
        if "i" in arg.split()[0] and arg.split()[0] != "ioio":
            i = "1"
            argu = (arg.split()[0])[:-1]
        else:
            argu = arg.split()[0]
        if argu in "nop jmp ioio ret":
            out = z_arg_enc(arg,i)
        elif argu in "bra be bne bl ble bg bge push inte lp lph store":
            out = m_arg_enc_b(arg,i)
        elif argu in "pull lpc lupc load":
            out = m_arg_enc_c(arg)
        elif argu in "cmp lu":
            out = d_arg_enc_c(arg,i)
        elif argu in "add sub awc swc mul mulh div mod nand nor and or":
            out = t_arg_enc(arg,i)
        else: raise KeyError(f"invalid opcode: {argu}")
        return(out)
    
prints = ""
def print_(string):
    global prints
    prints += (string)
    prints += "\n"


def main(lines):
    global register_remap
    global map_
    global constants
    output = ""
    labels = []
    instruction_aliases = []
    lines = lines.split("\n")
    linecount = 0
    linecount2 = 1
    linecount3 = 1
    labelcount = 0
    instruction_alias = []
    for line in lines: #label prepass
        print_(f"encoding prepass {linecount3}: {line}")
        line = line.lstrip()
        if line != "":
            if line[0] != ";":
                if line[0] == ">": #saving of labels
                    if ";" in line:
                        labels.append(line[1:line.find(";")])
                    else:
                        labels.append(line[1:])
                    labels.append(labelcount)
                elif line[0] == "<": #loading of labels
                    labelcount += 5
                elif line[0] == "#": #define aliases
                    instruction_alias.append(line[line.find(" "):line.find(" : ")])
                    instruction_alias.append(line.count("/n")+1)
                elif line[0:line.find(" ")] in instruction_alias: #loading of aliases
                    labelcount += instruction_alias[instruction_alias.index(line[0:line.find(" ")])+1]
                elif line[0] == "/":
                    try:
                        labelcount += len(line[1:line.find(";")])/32
                    except:
                        labelcount += len(line[1:].strip())/32
                elif line[0] == "@":
                    try:
                        labelcount += len(line[1:line.find(";")])/32
                    except:
                        labelcount += len(line[1:].strip())/32
        linecount3 += 1
    print_("\n encoding \n")
    for line in lines:
        line = line.lstrip()
        out = ""
        for char in line:
            if char == ";":
                break
            out += char
        print_(f"encoding line {linecount2}; {linecount}: {line}")
        if out != "":
            if out[0:9] == "%REGISTER": #register renaming
                register_remap.append(out.split()[3])
                map_.append(out.split()[1])
            elif out[:out.find(" ")] in opcodes: #handle non immediate opcodes
                output += enc(out)
                linecount += 1
            elif out[:out.find(" ")-1] in opcodes: #handle immediate opcodes
                output += enc(out)
                linecount += 1
            elif out[0] == "{":
                out = out.rstrip()
                output += ("0000000"+bin(int(out[1:-1]))[2:])[-8:]
                linecount += 0.25
            elif out[0] == ">": #label saving
                print_(f"label on line {linecount2}; {linecount}:")
            elif out[0] == "<": #label loading
                index = labels[labels.index(out[1:])+1]
                output += enc(f"addi r29,{index%65536},r29")
                output += enc(f"lui r29,{index//65536%65536}")
                output += enc(f"addi r30,{index//65536//65536%65536},r30")
                output += enc("lp r29")
                output += enc("lph r30")
                linecount += 5
            elif out[0] == "/":
                output += out[1:].strip()
                linecount += len(out[1:])/32
            elif out[0] == "@": 
                for char in out[1:]:
                    output += ("0000000"+bin(ord(char))[2:])[-8:]
                    linecount += 0.25
            elif out[0:6] == "#ALIAS": #instruction aliases
                temp = out.find(" : ") 
                start = out.find(" ")
                mid = out.find("%")
                if mid == -1:
                    mid = out.find(" : ")
                alias = out[start+1:mid-1]
                instruction = out[temp+3:]
                instruction_aliases.append(alias)
                instruction_aliases.append(instruction)
            elif out[0:6] == "#CONST": #untested constant code
                out = out.split()
                constants.append(out[1])
                constants.append(out[3])
            if out.find(" ") != -1:
                if out[0:out.find(" ")] in instruction_aliases: #handle instruction aliases
                    out = out.replace(","," ")
                    alias = out[0:out.find(" ")]
                    instructions = instruction_aliases[instruction_aliases.index(alias)+1]
                    out2 = out.split()
                    registers = []
                    for i in range(out.count(" ")):
                        registers.append(out2[i+1])
                    for a in "abcdefghijklmnopqrstuvwxyz":
                        if "%"+a in instructions:
                            reg = registers.pop()
                            instructions = instructions.replace(f"%{a}",reg)
                    linecount += instructions.count(" /n ")+1
                    instructions = instructions.replace(" /n ","\n").replace(","," ").split("\n")
                    for j in instructions:
                        output += enc(j)
            else: 
                if out in instruction_aliases: #handle zero argument instruction aliases
                    instructions = instruction_aliases[instruction_aliases.index(out)+1]
                    linecount += instructions.count(" /n ")+1
                    instructions = instructions.replace(" /n ","\n").replace(","," ").split("\n")
                    for j in instructions:
                        output += enc(j)
        linecount2 += 1
    return output

output = main(file) #REPLACE THIS WITH YOUR ASSEMBLY
