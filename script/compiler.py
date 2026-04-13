file_to_load = "./example.txt"

null = "\33[0m"
red = "\33[31m"
green = "\33[32m"
yellow = "\33[33m"
blue = "\33[34m"
magenta = "\33[35m"
white = "\33[36m"

with open(file_to_load,"r") as file:
    foo = file.readlines()

tokens = []

print(f"{yellow}starting tokenization{null}")

for line in foo:
    #tokenize
    token = " "
    for char in line: #space out operands and shit
        match(char):
            case "(": token += " ( " #parens, brackets, braces(for parsing)
            case ")": token += " ) "
            case "[": token += " [ "
            case "]": token += " ] "
            case "{": token += " { "
            case "}": token += " } "
            case "!": token += " ! " #logical not
            case "@": token += " @ " #reference
            case "#": preprocessor = True; token += "#"
            case "$": token += " $ " #dereference
            case "%": token += " % " #mod
            case "^": token += " ^ " #xor
            case "&": token += " & " #and
            case "*": token += " * " #mul
            case "+": token += " + " #add
            case "-": token += " - " #sub
            case "/":
                if token[-2:] != "/ ":
                    token += " / "
                else:
                    token = token[:-2]
                    break
            case "~": token += " ~ " #bitwise not
            case ",": token += " , " #comma
            case "=": # allow for == to be tokenized correctly
                if token[-2:] != "= ":
                    token += " = "
                else:
                    token = token[:-1]
                    token += "= "
            case _: token += char #add letters and numbers freely

    token = token.lstrip().rstrip()
    if token != " ":
        print("token:" +token)
        
        tokens.append(token)


print(f"{green}tokenization finished sucessfully.\n{yellow}starting preprocessing{null}")



packages = ""
flags = [0,1,1,1,1,1]
variables = []
functions = []
defines = []

#flag definitions
"""
name_overloading
funct_overloading
warnings
highlight
error_squiggles
recursion_limit
"""

for token in tokens: #preprocessor
    token2 = token.split()
    if token == "": #skip empty tokens
        continue
    if token[0] == "#":
        #preprocess
        if "#include" in token2[0]:
            packages += token2[1][1:-1]
            packages += " "
        if "#cflags" in token2[0]:
            flags = token2[1:]
        if "#def" in token2[0]:
            defines.append(token2[1])
            defines.append(token2[3])
    if token2[0] == "def":
        functions.append(token2[2])
        functions.append(token2[1])
        temp = len(token2) - 6
        for i in range(temp):
            functions.append(token2[i+4])
        functions.append("end")
    if token2[0] in "u8 u16 u32 u64 i8 i16 i32 i64 bool char":
        if not token2[1] in variables:
            variables.append(token2[1]) #append variablle name and type
            variables.append(token2[0])


print(f"{green}preprocessing finished sucessfully. results:{null}")

print(f"{blue}Tokens:{null}")
print(tokens)

print(f"{blue}Packages:{null}")
print(packages)

print(f"{blue}Flags:{null}")
print(flags)

print(f"{blue}Variables:{null}")
print(variables)

print(f"{blue}Definitions:{null}")
print(defines)

print(f"{blue}functions:{null}")
print(functions)

instructions = ""
const_split = 2**16

for token in tokens:
    line = token.split()
    if token == "":
        continue
    if token[0] == "#":
        continue
    if line[0] == "def":
        instructions += f"<_funct_{line[2]}\n"
    if line[0] == "if":
        if line[2].isdigit():
            instructions += ""
        instructions += "cmp r1,r2"









print(f"{green}Done!{null}")
