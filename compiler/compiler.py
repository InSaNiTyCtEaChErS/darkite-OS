#functions:
#keep track of local variable count when inside a function, and decrement the stack pointer by that count upon returning
#remember to make sure to parse arguments in order


#recursively call the argument parser to evaluate function calls inside of expressions, as well as ordering the arguments properly.
#argument order:
#*,/,% +,-, ==,!=,<=, functions

#the argument parser should read all tokens and parse them in order, resolving any tokens in parentheses through recursive calls of itself.


#make sure to handle libraries by including them at the line they're mentioned at, and jumping over their section.



#various tokens:

#variable operations
#[MEM store] addr: {variable_offset} + [stack_offset] + [working_stack]; width: 32
#[MEM load] addr: {variable_offset} + [stack_offset] + [working_stack]; arg: 1; width: 32

#operations (more than are listed here)
#[OP add]
#[OP or]
#[OP cmp]
#[OP mov] dest: arg_1

#conditional execution (more than are listed here)
#[JMP] condition: less_equal; label: {immediate|label}
#[LABEL] {label}
#may be parsed into a branch operation by the backend

#stack operations (more are possible than shown)
#[OP push] width: 8; arg: 1
#[OP pull] width: 64; arg: fp
#[OP push] width: 64; arg: flags

#immediates (more are possible than shown)
#[IMM] arg: 1; value: 3
#[IMM] arg: 2; value: 11
#[IMM] arg: 1; value: 314159

#functions
#[CALL] label: {label}
#[RET]

#specialty operations
#[ASM] {assembly}
#[LOG] {variable}
#[DUMP]
#[COMMENT] {comment}



secrets_text = "backends/secrets.txt"

with open(secrets_text) as file:
    secrets = file.read()


variable_names = []
variable_sizes = []
byte_indices = [0]

struct = False
struct_name_ = ""
structs = [] #list of struct names
struct_variables = []#insert a list of struct variables in here
struct_variable_sizes = [] #insert a list of variable sizes for the struct
struct_substruct = [] #insert a list of substruct definition names
struct_temp_var = []
struct_temp_sizes = []
struct_temp_substruct = []


global_names = []
global_sizes = []
global_indices = [0]

definitions = []
def_data = []

functions = []
function_inputs = []

recursion_limit = 16
recursion_index_include = 0
recursion_index = 0

op_counter = 0
op_stack = []

output = ""

macros = []
types = []
type_alters = []

last_condition_if = []
cond_temp_if = ""
last_condition_for = []
cond_temp_for = ""

linecount = 1-secrets.count("\n") #debugging thingies
error = False
comment = False


#colors
null = "\33[0m"
red = "\33[31m"
green = "\33[32m"
yellow = "\33[33m"
blue = "\33[34m"
magenta = "\33[35m"
white = "\33[36m"

def parse_expression(lines): #remember parentheses are on top so they would get a 0 value. -1 refers to a variable token
    precedence = {
        "@":1, #reference
        "%":1, #dereference
        "&":2, #and
        "|":2, #or
        "!":2, #not
        "^":2, #xor
        "*":3, #mul
        "/":3, #div
        "+":4, #add
        "-":4, #sub
        "==":5,#equal
        "!=":5,#notequal
        "<": 5,#less
        "<=":5,#lesseq
        "=<":5,#lesseq
        ">": 5,#greater
        ">=":5,#greatereq
        "=>":5 #greatereq
        }
    
    #TODO: FINISH THIS AS WELL

    #pointer notes:
    #to create a pointer, we get the address of the variable (by using the list we already have)
    #and to dereference a pointer we load from that address in the var stack


def type_handler(size):
    global types
    global type_alters
    for i in range(len(types)):
        if size == types[i]:
            return(int(type_alters[i]))
    raise KeyError(f"invalid type: {size}")




def struct_handler(lines,name):

    sizeof = lines[0]
    if name == "":
        lines = lines[1:]
    global recursion_limit
    global recursion_index

    if recursion_index >= recursion_limit:
        raise RecursionError("struct handler recursed too many times")
    recursion_index += 1

    global structs
    global struct_name_
    global struct_variables
    global struct_variable_sizes
    global struct_substruct

    global variable_names
    global variable_sizes
    global byte_indices

    if name == "":
        struct_name_ = lines[1]

    struct_def_name = lines[0] #get the struct's source name
    struct_name = lines[1] #get  the struct's variable name
    try:
        struct_variable = lines[3] #get the variable to set
    except:
        struct_variable = "@NULL"
    if not struct_name in variable_names:
        struct_vars = struct_variables[structs.index(struct_def_name)] #get the variables of a struct
        struct_var_sizes = struct_variable_sizes[structs.index(struct_def_name)] #get the sizes of the variables in the struct
        struct_substruct_ = struct_substruct[structs.index(struct_def_name)] #get the name of the struct if it's nested

        for i in range(len(struct_vars)):
            struct_var = struct_vars[i]
            struct_var_size = struct_var_sizes[i]
            struct_var_size_2 = struct_substruct_[i]
            if struct_var_size == "struct":
                struct_handler((struct_var+" "+struct_var_size_2).split(),name+struct_name+"@")
            else:
                size = type_handler(struct_var_size)
                variable_names.append(name+struct_name+"@"+struct_var)
                variable_sizes.append(size)
                byte_indices.append(byte_indices[-1]+size)
        
    if not struct_variable == "@NULL" and name == "": #assign one of the values of the struct, if we selected one, but never on any recursive instances
        value = lines[2:]

        names = False #is the next token a struct index name?
        name_list = struct_name

        for token in value: #get the full path of the struct's name
            token = str(token)
            if names and not token == "]":
                name_list += "@"+token
            else:
                names = False
            if token == "[": #set name to true if we expect a name
                names = True
            if token == "=": #break on equals to avoid parsing into the expression
                break
        names = name_list

        equals = False
        expression = ""
        for token in value:
            if token == "=":
                equals = True
                continue
            if equals== False:
                continue
            expression += " "+token+" "

        set_var(sizeof+" "+names+" = "+expression)



def set_var(line):
    lines = line.split()

    is_global = False
    is_struct = False
    
    global variable_names
    global variable_sizes
    global byte_indices

    global global_names
    global global_sizes
    global global_indices

    global structs
    global struct_variables
    global struct_variable_sizes

    global definitions
    global def_data

    output = ""

    if lines[0] == "global":
        lines = lines[1:]
        is_global = True
    
    if lines[0] == "struct":
        lines = lines[1:]
        is_struct = True

    #get the size in bytes of the variable
    size = type_handler(lines[0])

    if not is_struct:
        try:
            if lines[2] == "[":
                size = size*int(lines[3])
                before_array = lines[0:2]
                try:
                    after_array = lines[5:]
                except:
                    after_array = []
                lines = before_array+after_array #remove the array designator
        except:
            size = size
        if is_global:
            if lines[1] not in global_names: #append the global variable if it doesn't exist
                global_names.append(lines[1])
                global_sizes.append(size)
                global_indices.append(global_indices[-1]+size)

        else:
            if lines[1] not in variable_names: #append the variable if it doesn't exist
                variable_names.append(lines[1])
                variable_sizes.append(size)
                byte_indices.append(byte_indices[-1]+size)

        equals = lines.index("=") #find equals, and handle the line to the right of the equals
        parse_expression(lines[equals+1:])

        dest_name = byte_indices[variable_names.index(lines[1])]
        output += "\n[IMM] arg: 2; value: 0\n[OP add]" #move argument 1 to dest so we can store it

        output += f"\n[COMMENT] var store {lines[1]}\n[MEM store] addr: {dest_name} + [stack_offset] + [pile_offset]; size: {str(size*8)}"#store dest at stack offset + pile offset(size of stack that's kept in a special location)
    else:
        struct_handler(lines,"")
    return(output)




def if_handler(line):
    global output
    global op_counter
    global last_condition_if

    line = line[line.find("(")+1:line.find(")")]
    lines = line.split()
    cond = line.find("=")
    cond = line[cond:cond+1]
    last_condition_if.append(cond)

    parse_expression(lines)

    output += f"\n[COMMENT] if statement\n[IMM] arg: 2; value: 1\n[OP cmp]\n[JMP] cond: not_equal; label: __if{str(op_counter)}" #comparison chain used to get the conditional
    out = (f"\n[LABEL] __if{op_counter}") #get the label for the if statement to jump to
    op_counter += 1

    return(out) #return the label for the if statement to jump to if the condition was not met

def else_handler():
    
    global output
    global op_counter
    global cond_temp_if

    cond_match = {
        "==":"not_equal",#equal
        "!=":"equal",#notequal
        "<": "greater_equal",#less
        "<=":"greater",#lesseq
        "=<":"greater",#lesseq
        ">": "less_equal",#greater
        ">=":"less",#greatereq
        "=>":"less" #greatereq
    }
    cond = cond_match[cond_temp_if]

    output += f"\n[COMMENT] else statement\n[JMP] condition: {cond}; label: _else{str(op_counter)}"

    op_stack.append(f"[LABEL] __else{str(op_counter)}")

    op_counter += 1



def for_handler(line):

    global op_stack
    global op_counter
    global output

    global last_condition_for

    expression = line[line.find("(")+1:line.find(")")] #get the actual part we care about
    setup = expression[0:expression.find(";")] #get the setup code
    index = len(setup) + 1 #get the index for the condition code
    condition= expression[index:]  #get the condition code
    index2 = condition.find(";") #find the end of condition
    end_statement = condition[index2+1:]
    condition = condition[0:index2]

    output += set_var(setup) #setup statement

    label = f"\n[COMMENT] for loop\n[LABEL] __for{op_counter}" #label before the if statement, so that we can jump back to it
    last_condition_for.append(f"__for{op_counter}")
    output += label #add the label to the output

    out = set_var(end_statement) + f"\n[JMP] condition: always; label: __for{str(op_counter)}" + if_handler("if"+condition) #add a jump and the end condition's label to the stack
    #we don't increment op-counter here because it's already incremented once with the if statement and we use a different label

    op_stack.append(out)



def continue_handler():
    global output
    global cond_temp_for
    
    output += "\n[COMMENT] continue\n[JMP] condition: always; label: " + cond_temp_for





def funct_handler(line,bool):

    global op_stack

    global definitions
    global def_data

    global functions
    global function_inputs

    lines = line.split()
    if bool == 0:
        #handle regular functions
        name = lines[1]
        parentheses = lines.index(")")
        variables = lines[3:parentheses]
        functions.append(name)
        function_inputs.append(variables)

    else:
        #handle definitions
        definitions.append(lines[1])
        def_data.append(lines[3])



def typedef_handler(lines):
    global types
    global type_alters

    types.append(lines[1])
    type_alters.append(lines[2])



def handle_line(line):
    global recursion_index_include
    global recursion_limit

    if recursion_index_include>=recursion_limit:
        raise(RecursionError("Too many recurses in include directory"))

    global struct
    global structs
    global struct_variables
    global struct_variable_sizes
    global struct_substruct

    global struct_temp_var
    global struct_temp_sizes
    global struct_temp_substruct

    global output
    global op_stack

    global last_condition_if
    global cond_temp_if
    global last_condition_for
    global cond_temp_for

    global null
    global red
    global yellow
    global green
    global blue
    global magenta
    global white

    global linecount
    global error
    global comment

    #tokenize
    token = " "
    previous_char = ""

    try:
        for char in line: #space out operands and shit
            if comment == True and (char == "/" and previous_char == "*"):
                comment = False
                continue
            if comment == True:
                previous_char = char
                continue
            match(char):
                case "(": token += " ( " #parens, brackets, braces(for parsing)
                case ")": token += " ) "
                case "[": token += " [ "
                case "]": token += " ] "
                case "{": token += " { "
                case "}": token += " } "
                case "!": token += " ! " #logical not (possibly part of a not equals but that's handled in equals)
                case "@": token += " @ " #reference
                case "#": token += "#"  #preprocessor shenanigans
                case "$": token += " $ " #dereference
                case "%": token += " % " #mod
                case "^": token += " ^ " #xor
                case "&": token += " & " #and
                case "*":
                    try:
                        if token[-2:] == "/ ":#multiline comment start
                            comment = True
                            token = token[:-2]
                        else:
                            token += " * " #mul
                    except:
                        token += " * " #mul as a fallback operation
                case "+": token += " + " #add
                case "-": token += " - " #sub
                case "/":
                    try:
                        if token[-2:] != "/ ":#div
                            token += " / "
                        else:
                            token = token[:-2] #single line comments
                            break
                    except:
                        token += " / " #div as a fallback operation
                case "~": token += " ~ " #bitwise not
                case ",": token += " , " #comma
                case "=": # allow for == to be tokenized correctly, as well as >= and shit
                    try:
                        if token[-2:] != "= "and token[-2:] != "< "and token[-2:] != "> "and token[-2:] != "!":
                            token += " = "
                        else:
                            token = token[:-1]
                            token += "= "
                    except:
                        token += " = "
                case "<":
                    try:
                        if token[-2:] != "= ":
                            token += " < "
                        else:
                            token = token[:-1]
                            token += "< "
                    except:
                        token += " < "
                case ">":
                    try:
                        if token[-2:] != "= ":
                            token += " > "
                        else:
                            token = token[:-1]
                            token += "> "
                    except:
                        token += " > "
                case _: token += char #add letters and numbers freely
            previous_char = char
        #strip leftover spaces and newlines
        token = token.lstrip().rstrip()
        if token != "": #if token not equals an empty string, parse token
            print(f"{blue}line {linecount}:{line}{null}")
            lines = token.split()

            if struct == False:
                if token[0] == "}": #allow for closing a statement at the begining of a line only
                    temp = op_stack.pop()
                    output += temp
                    if "if" in temp: #handle setting up the last_condition variable correctly on if or for loop end
                        last_condition_if.pop()
                    if "for" in temp: #handle setting up the last_condition variable correctly on if or for loop end
                        last_condition_for.pop()
                    lines = lines[1:]
                try:
                    cond_temp_if = last_condition_if[-1]
                except:
                    cond_temp_if = ""
                try:
                    cond_temp_for = last_condition_for[-1]
                except:
                    cond_temp_for = ""
                if lines != []:
                    match lines[0]:
                        case "if":
                            #if statements
                            op_stack.append(if_handler(token))
                        case "else":
                            else_handler()
                        case "for":
                            #for loops
                            for_handler(token)
                        case "continue":
                            continue_handler()
                        case "def":
                            #handle functions
                            funct_handler(token,0)
                        case "#def":
                            #handle "preprocessor" tokens
                            funct_handler(token,1)
                        case "#typedef":
                            #handle type definitions/aliases
                            typedef_handler(lines)
                        case "struct":
                            #handle structs
                            if lines[2] == "{":
                                structs.append(lines[1])
                                struct = True
                            else:
                                set_var(token)
                        case "log":
                            #log something to the log file
                            output += f"\n[LOG] {lines[1]}" #insert log statements
                        case "asm":
                            #add raw assembly to the mix
                            output += f"\n[ASM] {line[3:]}" #insert assembly
                        case "RDUMP":
                            #handle register dumps from the sim
                            output += "\n[DUMP]"
                        case "#include":
                            #handle file inclusion
                            out = ""
                            for token in lines[1:]: #make the list of tokens back into a string
                                out += token
                            compile(out)
                        case _:
                            #variables
                            set_var(token)
            else:
                if line == "}":
                    struct = False
                    #append the temporaries
                    struct_variables.append(struct_temp_var)
                    struct_variable_sizes.append(struct_temp_sizes)
                    struct_substruct.append(struct_temp_substruct)
                    #reset the temporaries
                    struct_temp_var = []
                    struct_temp_sizes = []
                    struct_temp_substruct = []
                else:
                    struct_temp_var.append(lines[1])
                    struct_temp_sizes.append(lines[0])
                    try:
                        struct_temp_substruct.append(lines[2])
                    except:
                        struct_temp_substruct.append("")
    except:
        print(f"{red}ERROR ON LINE {linecount}: {line}{null}")
        error = True
    linecount += 1


def compile(string):
    global error
    global file_to_write
    global output
    strings = string.split("\n")
    for line in strings:
        handle_line(line)
    if not error:
        print(f"{magenta}done!{null}")
        with open(file_to_write,"w") as file:
            file.write(output)

    else:
        print(f"{red}Build finished with errors.{null}")
    



file_to_open = "./programs/testing.cyth"
file_to_write = "./temporary_files/temporary.txt"

with open(file_to_open) as file:
    foo = file.read()

foo = secrets + foo

compile(foo)
