[fields]

reg
zr  00000 //hardwired to zero
r1  00001
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
r19 10011
r20 10100
r21 10101
r22 10110
r23 10111
r24 11000
r25 11001
r26 11010
r27 11011
r28 11100
r29 11101
imm 11110   //DO NOT USE. HARDWIRED TO IMMEDIATE BITS
flags 11111 //hardwired to the 4 flags. carry, eq, low,  less (unsigned, signed)


alu
and 0000 //and two values
shl 0001 //not input a
or  0010 //or two values
xor 0011 //xor two values
add 0100 //add two values
awc 0101 //add with carry flag
unu 0110
unu 0111
andn 1000 //and with not of second value
unu  1001 
orn  1010 //or with not of second value
xnor 1011 //xnor two values
sub  1100 //subtract two values
swc  1101 //subtract with carry flag
unu  1110 
unu  1111 

bra
nop 0000
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
unu 1100
unu 1101
unu 1110
unu 1111


[instructions]

/*
* OPERATIONS & OPCODE
* 0:15 ALU
* 16:31 BRA
* 32 load  // load from cache
* 33 store // store to cache
* 34 inte  // set an interrupt address
* 35 iread // read an interrupt value
* 36 out   // output a byte to OUT
* 37 biin  // bidirectionally read a byte in
* 38 biout // bidirectionallly write a byte out
* 39 LUI   // RISC-V like load upper immediate instruction
* 40 cmp   // compare two registers.
* 41 call  // call to a label
* 42 ret   // return from a label or interrupt
* 43 push  // push a value to stack
* 44 pull  // pull a value from stack
* 45 user  // switch back to user mode and reset the timer for switching to kernel mode
* 46 
* 47
*/

/*
* INTERUPT TYPES AND VALUES     value produced: (16 bit, sign extended to 32)
* 0 INVALID INSTRUCTION         -1
* 1 EXTERNAL MEMORY READ DONE   value of byte read
* 2 STACK OVER/UNDERFLOW		-2
* 3 FP OVER/UNDERFLOW			-3
* 4 KEYBOARD					ACSCII value of pressed key (0-255)
* 5-15 RESERVED FOR FUTURE USE  undecided
*/



//NOTES:

/*
* reset being held for one cycle indicates memory read done
* reset being held for two cycles indicates keyboard input
* reset being held for 3+ cycles indicates an interrupt value associated with the number of cycles held.
- beyond 15 triggers a proper reset
*/

//memory operations
load %a(reg), %b(reg)
00000000000100000bbbbbaaaaa00000
//load from address %a to regisster %b

loadi %a(immediate), %b(reg)
aaaaaaaaaaa100000bbbbb1111000000
//load from address %a to regisster %b

store %a(reg), %b(reg)
0000000000010000100000aaaaabbbbb
//store value %b at address %a

storei %a(immediate), %b(reg)
aaaaaaaaaaa1000010000011110bbbbb
//store value %b at address %a


//interrupts
inte %b(reg), %a(reg)
0000000000010001000000bbbbbaaaaa
//set interrupt %b to address %a

intei %b(reg), %a(immediate)
aaaaaaaaaaa10001000000bbbbb11110
//set interrupt %b to address %a


//Input/Output

iread %a(reg)
00000000000100011aaaaa0000000000
//read an interrupt's value

out %a(reg), %b(reg)
0000000000010010000000aaaaabbbbb
//output a byte from %a, shifted right by 8*%b

outi %a(reg), %b(immediate)
bbbbbbbbbbb10010000000aaaaa11110
//output a byte from %a, shifted right by 8*%b

biin %a(reg)
00000000000100101aaaaa0000000000
//bidirectional INPUT read

biout %a(reg)
000000000001001100000000000aaaaa
//bidirectional OUTPUT write

lui %a(immediate) %b(reg)
aaaaaaaaaaa100111bbbbbaaaaa00000
//load upper immediate. encoded specially.

//special

cmp %a(reg), %b(reg)
0000000000010100000000aaaaabbbbb
//compare two registers and set flags

cmpi %a(reg), %b(immediate)
bbbbbbbbbbb10100000000aaaaa11110
//compare a register and immediate, and set flags.

call 
00000000000101001000000000000000
//call the function in pointer

ret
00000000000101010000000000000000
//return from a function

push %a(reg)
000000000001010110000000000aaaaa
//push a register to the stack

pull %a(reg)
00000000000101100aaaaa0000000000
//pull a register from the stack

user
00000000000101101000000000000000
//switch to user mode and continue executing. should be followed by a RET instruction


//alu
%a(alu) %b(reg), %c(reg), %d(reg)
0000000000000aaaadddddcccccbbbbb
//perform the alu operation %a on the registers %b and %c, and store it at %d

%a(alu)i %b(reg), %c(immediate), %d(reg)
ccccccccccc00aaaaddddd11110bbbbb
//perform the alu operation %a on the register %b and immediate %c, and store it at %d

//bra
%a(bra) %b(reg)
0000000000001aaaa00000bbbbb00000
//branches forwards or backwards a signed ammount

%a(bra)i %b(immediate)
bbbbbbbbbbb01aaaa000001111000000
//branches forwards or backwards a sign-extended immediate ammount
