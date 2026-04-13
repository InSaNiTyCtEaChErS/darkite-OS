# darkite-OS
simple assembly based operating system for my custom cpu. includes assembly documentation for any contributors.



# useful functions when writing code for this

### THE MANUAL

https://github.com/InSaNiTyCtEaChErS/darkite-OS/blob/main/ASM.txt


### external functions

https://github.com/InSaNiTyCtEaChErS/darkite-OS/blob/main/external%20functions.asm


# assembler functions

### #ALIAS:
```
#ALIAS {instruction} %a %b... : {instructions with %a,b,c replacing registers in desired order}
#ALIAS means comment this line out and define an instruction alias.
{instruction} is the name for the alias. must be one continuous word, no spaces.
NOTE: the %a,%b... must be in order!
%a/%b are the argument(s) of the instruction. you can have up to 52 of these.
{instructions with %a,b,c replacing registers in desired order} is the instructions to
actually execute, with %a,%b... being replaced with supplied values.
```
example:
```
#ALIAS clear %a : sub %a,%a,%a;the spaces around the : are necessary
```
### #CONST:
```
#CONST name = register/immediate
name can be any continuous string of ascii excluding spaces. AVOID REGISTER NAMES.
note: the program does not differentiate immediate and register constants. you do.
```
example:
```
#CONST input = r1
#CONST banana = 314159
```
### {int}
```
{0}
insert 8-bit integers directly into data. 
```
example:
```
{69}
{40}
{20}
{0}
```
### @characters
```
@I AM A STRING!!!
insert 8-bit ascii characters directly into data.

THESE INCLUDE ANY TRAILING SPACES
```
example:
```
@darkite ;comment to fix parsing
```
### LABELS
```
>define_a_label_like_this

<load_a_label_like_this

labels can be used before they're defined
```
example
```
<jump_to_a_label_like_this ;with a jump instruction
jmp

<call_a_label_like_this ;with a call instruction
call
```

### #RESBY
```
reserve some number of bytes as zero, also useful for padding large areas
```
example
```
resby 512 ;reserves 512 bytes for whatever
```
### /01010101
```
add some bits directly into the stream. should be branched or jumped over, unless you are using this to encode weird instructions.
DO NOT PUT SPACES IN THE STRING. IT WILL BREAK THE SIM.
```
example
```
/00110001
```

# example codes for the language

script/example.txt
