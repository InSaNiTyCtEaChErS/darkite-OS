# darkite-OS
simple assembly based operating system for my custom cpu. includes assembly documentation for any contributors.

# useful functions when writing code for this

### #ALIAS:
```
#ALIAS {instruction} %a %b... : {instructions with %a,b,c replacing registers in desired order}
#ALIAS means comment this line out and define an instruction alias.
{instruction} is the name for the alias. must be one continuous word, no spaces. NOTE: the %a,%b... must be in order!
%a/%b are the argument(s) of the instruction. you can have up to 52 of these.
{instructions with %a,b,c replacing registers in desired order} is the instructions to actually execute, with %a,%b... being replaced with supplied values.
```
example:
```
#ALIAS clear %a : sub %a,%a,%a;the spaces around the : are necessary
```
### #CONST:
```
#CONST name = register
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
insert 8-bit integers directly into data. MAKE SURE TO KEEP DATA DOUBLE WORD ALIGNED. PC CANNOT BRANCH OR JUMP OFF OF WORD ALIGNMENT.
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
insert 8-bit ascii characters directly into data. MAKE SURE TO KEEP DATA DOUBLE WORD ALIGNED. PC CANNOT BRANCH OR JUMP OFF OF WORD ALIGNMENT.

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
<jump_to_a_label_like_this
jmp
<call_a_label_like_this
call
```


