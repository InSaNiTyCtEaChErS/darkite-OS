[fields]

reg
zr  00000 //hardwired to zero
r1  00001 //gprs
r2  00010
r3  00011
r4  00100
r5  00101
r6  00110
r7  00111
r8  01000
r9  01001
r10 01010
r11 01011
r12 01100
r13 01101
r14 01110
r15 01111
r16 10000
r17 10001
r18 10010
scr 10011 //scratch register, used for macros when needed
fp 10100 //frame pointer and stack pointer
sp 10101
lr  10110 //link register + alternate link register
alr 10111
syslink 11000 //system call link register
sysS 11001 //syscall ID
sysA 11010 //syscall arg a
sysPB0 11011 //syscall pointer arg
sysPB1 11100 //syscall pointer arg, cont.
ks 11101    //DO NOT USE. KERNEL WILL NULL THIS REGISTER RANDOMLY DURING EXECUTION.
imm 11110   //DO NOT USE. HARDWIRED TO IMMEDIATE BITS
flags 11111 //hardwired to the 4 flags. carry, eq, low,  less (unsigned, signed). 
//only has 4 bits because of this.


alu
and 0000 //and two values
not 0001 //not input a
or  0010 //or two values
xor 0011 //xor two values
add 0100 //add two values
awc 0101 //add with carry flag
shl 0110 //shift left x bits
shr 0111 //shift right x bits
andn 1000 //and with not of second value
unu  1001
orn  1010 //or with not of second value
xnor 1011 //xnor two values
sub  1100 //subtract two values
swc  1101 //subtract with carry flag
rol  1110 //rotate left x bits
ror  1111 //rotate right x bits

bra
nop 0000 //no operation.
bra 0001 //branch always
beq 0010 //branch equal
bne 0011 //branch not equal
bl  0100 //branch less (signed)
bge 0101 //branch greater equal
ble 0110 //branch less equal
bg  0111 //branch greater
bb  1000 //branch below (unsigned)
bae 1001 //branch above equal
bbe 1010 //branch below equal
ba  1011 //branch above
b0  1100 //useless branches
b1  1101
b2  1110
jmp 1111 //jump instruction. used with branch and link instructions for calling and returning.

mem
rll 00  //read low bound 
rhl 01  //read high bound 
wll 10  //write low bound 
whl 11  //write high bound


[instructions]

/*
* OPERATIONS & OPCODE. FOR RESTRICTED MODE DETAILS, CHECK THE NEXT SECTION.
*
* 0:15 ALU %a(reg), %b(reg|imm), %c(reg) //ALU opcodes. refer to ALU field.
* 16:31 BRA %a(reg)                      //branch opcodes. refer to BRA field.
* 32 load %a(reg), %b(reg|imm)  // load from cache
* 33 store %a(reg), %b(reg|imm) // store to cache
* 34 inte %a(reg), %b(reg|imm)  // set an interrupt address. privliged.
* 35 iread %a(reg)              // read an interrupt value. unprivliged for some reason.
* 36 ptr %a(reg), %b(imm)     // set or read a pointer value. privliged.
* 37 rpc %a(reg)           // read the 32 bit program counter
* 38 mem %a(reg), %b(imm)  // edit the memory bounds registers. privliged. takes an immediate to decide
*                               whether to write/read(2/0) and whether to use the low or high bound
* 39 LUI %a(reg), %b(imm)  // RISC-V load upper immediate instruction
* 40 cmp %a(reg), %b(reg|imm)  // compare two registers, or a reg and an imm.
* 41 syscall               // syscall.
* 42 sysret                // sysret. privliged.
* 43 user                  // switch to user mode and jump to user program counter
* 44 supc                  // set user program counter
* 45 rupc                  // read user program counter.
* 46 lli %a(reg), %b(imm)  // load lower 21 bits of a register with an immediate
* 47 HALT                  // halt until next reset. privliged.
* 48
* 49
* 50
* 51
* 52
* 53
* 54
* 55
* 56
* 57
* 58
* 59
* 60
* 61
* 62
* 63
*/

/*
* RESTRICTED INSTRUCTIONS:
only MEM, SYSRET, INTE, PTR, and HALT are restricted in user mode. everything else is fair game.
*/

/*
* INTERUPT TYPES AND VALUES      value produced: (16 bit, sign extended to 32 bit)
* 0 INVALID INSTRUCTION          -1
* 1 SERIAL INPUT                 value of input byte
* 2 STACK OVER/UNDERFLOW		 -2
* 3 UNPRIVLEGED INST ATTEMPTED   -3
* 4 KEYBOARD					 ACSCII value of pressed key (0-255)
* 5 USER MODE SWITCH             0
* 6 page fault (x86-like)        -4
* 7 mouse input                  value of button(undecided)
* 8-15 RESERVED FOR FUTURE USE   undecided
*/



/*
* #### NOTES ################################################################################
* FLAGS
*   carry flag is only used on awc and swc, and is stored as the lowest bit in the flags register
*     otherwise carry is assumed to be 0.
*   equals flag is only set/cleared on CMP and is the second lowest bit in the flags register
*   lower flag(unsigned) is the third lowest bit in the flags register and is only set/cleared on CMP
*   less flag(signed) is the fourth lowest bit in the flags register and is only set/cleared on CMP
*
* IMMEDIATE AND FLAGS LOADING
*   immediate can only be loaded as the second argument
*   if you try to load immediate from the first argument, it will load from a hidden "imm" register.
*   if you try to store to "imm", it will store to this hidden register. DO NOT UTILIZE THIS.
*     WHY? BECAUSE KERNEL WILL NOT SAVE THIS "REGISTER" FOR YOU.
*   flags can be safely loaded as either argument, despite only being 4 bits.
* 
* INTERRUPT DETAILS
*   all interrupts set the hidden kernel mode register to 0(kernel mode) and switch to kernel pc
*     and overwrite kernel pc with a varying value if not already in kernel mode.
*     this is equivilant to having kernel mode be an interrupt mask.
*     IREAD still functions in kernel mode though.
*
*   INVALID INSTRUCTION EXCEPTION:
*     triggered when mode(top two bits of opcode) is set to 0b11
*
*   SERIAL INPUT INTERRUPT:
*     triggered whenever the serial port sends in data
*
*   STACK OVER/UNDERFLOW EXCEPTION:
*     triggered when stack overflows or underflows
*
*   UNPRIVLIGED INST ATTEMPT EXCEPTION:
*     triggered when user programs try to use a privliged instruction
*
*   KEYBOARD INTERRUPT:
*     triggered whenever the keyboard sends a key value in ASCII.
*
*   USER MODE SWITCH INTERRUPT:
*     occours after a dedicated number of cycles in user mode have passed.
*
*   PAGE FAULT EXCEPTION:
*     occours whenever a program tries to write or read outside of it's memory boundaries
*
*   MOUSE INPUT INTERRUPT:
*     occours whenever the mouse sends input data.
*
* PIPELINING + SUPERSCALAR + BRANCH PREDICTION+ OUT OF ORDER:
*   pipelining should be split into three stages. 
*     fetch+writeback
*     decode+load registers
*     execute
*   branch prediction should predict all branches taken
*   superscalar execution shall execute instructions in the same way as normal,
*     just executing extra ALU operations when possible.
*   This is not an Out Of Order architecture. there is no FENCE instruction/similar availiable.
*
* EXTRAS:
*   DATA BUS WIDTH: 32 bits
*   ALU WIDTH: 32 bits
*   INSTRUCTION LOAD WIDTH: 32 bits
*   DATA LOAD/STORE WIDTH: 32 bits
*/


// INSTRUCTION DEFINITIONS


//MEMORY OPERATIONS

load %a(reg), %b(reg)
00000000 000 100000 bbbbb 00000 aaaaa 
//loads address %a to reg %b. loads starting at 0 in kernel mode and starting at 2^15 in user mode.

loadi %a(immediate), %b(reg)
aaaaaaaa aaa 100000 bbbbb 11110 00000
//loads address %a to reg %b. loads starting at 0 in kernel mode and starting at 2^15 in user mode.

store %a(reg), %b(reg)
00000000 000 100001 00000 aaaaa bbbbb 
//stores %b at %a in cache. stores starting at 0 in kernel mode and starting at 2^15 in user mode.

storei %a(immediate), %b(reg)
aaaaaaaa aaa 100001 00000 11110 bbbbb
//stores %b at %a in cache. stores starting at 0 in kernel mode and starting at 2^15 in user mode.

ptri %a(reg), %b(immediate)
%c = %a
bbbbbbbb bbb 100100 aaaaa 11110 ccccc
//deals with the pointer and it's associated weirdness. privliged.

<%a(label)
aaaaaaaa aaa 100111 11101 aaaaa aaaaa aaaaaaaa aaa 000010 11101 11110 11101 00000000 010 100100 00000 11110 11101 aaaaaaaa aaa 100111 11101 aaaaa aaaaa  aaaaaaaa aaa 000010 11101 11110 11101 00000000 011 100100 00000 11110 11101
//just a very long macro to load a label.



//I/O OPERATIONS

inte %a(reg), %b(reg)
00000000 000 100010 00000 aaaaa bbbbb
//set an interrupt type (chosen by a register) to a value. privliged.

intei %a(immediate), %b(reg)
aaaaaaaa aaa 100010 00000 11110 bbbbb
//set an interrupt type (chosen by an immediate) to a value. privliged.

iread %a(reg)
00000000 000 100011 aaaaa 00000 00000
//read the last interrupt value.



//SPECIAL OPERATIONS

rpc %a(reg)
00000000 000 100101 aaaaa 00000 00000
//read kernel program counter. privliged.

rupc %a(reg)
00000000 000 101101 aaaaa 00000 00000
//read user program counter.

memi %a(reg), %b(mem)
00000000 bbb 100110 aaaaa 11110 aaaaa
//this instruction has no register variant. just used for setting up memory boundaries in hardware.
//do not ask how it works.

lui %a(reg), %b(immediate)
bbbbbbbb bbb 100111 aaaaa bbbbb bbbbb
//RV32/64I - based LUI instruction, loads upper 21 bits with a value.
//use an ORI after this to set the lower 11 bits.







//COMPARISON INSTRUCTIONS

cmp %a(reg), %b(reg)
00000000 000 101000 11111 bbbbb aaaaa
//compare two registers. stores the result to flags.

cmpi %a(reg), %b(immediate)
bbbbbbbb bbb 101000 11111 11110 aaaaa
//compare a register and an immediate. stores the result to flags.

cmps %a(reg), %b(reg), %c(reg)
00000000 000 101000 ccccc bbbbb aaaaa
//compare two registers. stores the result to any register. stands for compare special.

cmpsi %a(reg), %b(immediate), %c(reg)
bbbbbbbb bbb 101000 ccccc 11110 aaaaa
//compare a register and an immediate. stores the result to any register.
//stands for compare special immediate.



//COMPLEX INSTRUCTIONS

syscall
00000000 000 101001 10011 00000 00000
//syscall actually stores pc+4 in the syslink register, used in sysret.

sysret
00000000 000 101010 00000 00000 10011
//privliged SYSRET instruction. always takes the syslink register as where to return to.

push %a(reg)
00000000 000 101011 00000 aaaaa 00000
//push a value to the stack. privliged.

pushi %a(immediate)
aaaaaaaa aaa 101011 00000 11110 00000
//push an immediate onto the stack.

pull %a(reg)
00000000 000 101100 aaaaa 00000 00000
//pull the last-pushed value from the stack.

lli %a(reg), %b(immediate)
bbbbbbbb bbb 101110 aaaaa bbbbb bbbbb
//load lower 21 bits of a register with an immediate. useful for immediating numbers from 0 to 2^21-1.

HALT
00000000 000 101111 00000 00000 00000
//halts the cpu. has to be written in all caps, unlike other instructions, which must be lowercase. privliged.





//alu

%a(alu) %b(reg), %c(reg), %d(reg)
00000000 000 00aaaa ddddd ccccc bbbbb
//perform the alu operation %a on the registers %b and %c, and store it at %d

%a(alu)i %b(reg), %c(immediate), %d(reg)
cccccccc ccc 00aaaa ddddd 11110 bbbbb
//perform the alu operation %a on the register %b and immediate %c, and store it at %d


//branches

%a(bra) %b(reg)
00000000 000 01aaaa 00000 bbbbb 11111
//branches forwards or backwards a signed ammount.

%a(bra)i %b(immediate)
bbbbbbbb bbb 01aaaa 00000 11110 11111
//branches forwards or backwards a sign-extended immediate ammount.

%a(bra)l %b(reg), %c(reg)
00000000 000 01aaaa ccccc bbbbb 11111
//branch and link using a register.

%a(bra)li %b(immediate), %c(reg)
bbbbbbbb bbb 01aaaa ccccc 11110 11111
//branch and link a sign-extended immediate amount.


%a(bra)s %b(reg), %d(reg)
00000000 000 01aaaa 00000 bbbbb ddddd
//branches forwards or backwards a signed ammount while also using any register instead of flags.

%a(bra)si %b(immediate), %d(reg)
bbbbbbbb bbb 01aaaa 00000 11110 ddddd
//branches a sign-extended immediate ammount while also using
//any register instead of flags for the flags input.

%a(bra)sl %b(reg), %c(reg), %d(reg)
00000000 000 01aaaa ccccc bbbbb ddddd
//branch and link using a register while also using any register instead of flags.

%a(bra)sli %b(immediate), %c(reg), %d(reg)
bbbbbbbb bbb 01aaaa ccccc 11110 ddddd
//branch and link a sign-extended immediate amount while also using 
//any register instead of flags for the flags input.
