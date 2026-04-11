[fields]

// i signifies immediate value is used

reg
r0  00000
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
r30 11110
flags 11111


alu
add 00000
awc 00001
sub 00010
swc 00011
nand 00100
and 00101
rol 00110
ror 00111
or  11010

bra
bra 01001
be  01010
bne 01011
bl  01100
bg  01101
bb  01110
ba  01111



[instructions]

/*
0:7 ALU //ALU operations
8 JUMP  //absolute jump
9:15 BRA //branches(and conditionals)
16 LOAD  //load from a cache page
17 STORE //store to a cache page
18 CACHE // cache a page of ram or hdd
19 SHOVEL // shovel a page of cache back to ram or hdd
20 CALl  // call a function
21 RET   // return from a function or interrupt
22 INTE  // set the interrupt destination for a type of interrupt
23 CMP   // compare
24 SUPC  // set user program counter
25 LUI   //load upper immediate
26 OR    //or two values together
27 USER  //set to user mode
28 push  //push a register
29 pull  //pull a register
30 IOBIT //send or receive a single bit of i/o
31 HALT  // HALTS THE CPU
*/





//alu ------------------------------------------------------
%a(alu) %b(reg), %c(reg), %d(reg)
00000000000aaaaa0dddddcccccbbbbb

%a(alu)i %b(reg), %c(immediate), %d(reg)
cccccccccccaaaaa1dddddcccccbbbbb


//interrupts------------------------------------------------

inte %b(reg), %a(reg) 
0000000000010110000000aaaaabbbbb
// set the current address to an interrupt of a chosen value

intei %a(reg), %b(immediate)
bbbbbbbbbbb10110100000bbbbbaaaaa



//memory operations ------------------------------------------

load %a(reg), %b(reg)
0000000000010000000000bbbbbaaaaa

loadi %a(immediate), %b(reg)
aaaaaaaaaaa10000000000bbbbbaaaaa

store %a(reg), %b(reg)
0000000000010001000000bbbbbaaaaa

storei %a(immediate), %b(reg)
aaaaaaaaaaa10001100000bbbbbaaaaa


//cache loads use pointer as where to load or store from/to, and rs1/imm as where to put it in cache
cache %a(reg)
0000000000010010000000aaaaa00000

cachei %a(immediate)
aaaaaaaaaaa10010000000aaaaa00000

shovel %a(reg)
0000000000010011000000aaaaa00000

shoveli %a(immediate)
aaaaaaaaaaa10011000000aaaaa00000



//special ----------------------------------------------------------------------------

cmp %a(reg),%b(reg)
0000000000010111000000bbbbbaaaaa

cmpi %a(reg),%b(immediate)
bbbbbbbbbbb10111100000bbbbbaaaaa

call 
00000000000101000000000000000000

ret
00000000000101010000000000000000

lui %a(reg), %b(immediate)
bbbbbbbbbbb110001 %a[4:0]bbbbb%a[4:0]

<%a(label|immediate)
%b = %a
%c = %a[31:16]
00000000000 00010 0 11110 11110 11110 bbbbbbbbbbb 000001 11110 bbbbb 11110 ccccccccccc 11000 1 11110 ccccc 11110

HALT 
00000000000111110000000000000000
// halts the cpu.

user 
00000000000110110000000000000000
// switch the OS to user mode and continue executing.


push %a(reg)
0000000000011100000000aaaaa00000

pushi %a(reg)
aaaaaaaaaaa11100100000aaaaa00000

pull %a(reg)
00000000000111010aaaaa0000000000

iobit %a(reg), %b(reg)
00000000000111100bbbbbaaaaa00000
// use %a for source and %b for dest. basically a second memory space, just in serial format.

iobiti %a(immediate), %b(reg)
aaaaaaaaaaa111100bbbbbaaaaa00000


supc %a(reg)
0000000000011000000000aaaaa00000
// set user pc to a register

supci %a(immediate)
aaaaaaaaaaa11000000000aaaaa00000
// set user pc to an immediate

//pc operations ---------------------------------------------
jmp
00000000000010000000000000000000 
// jumps to the pointer

%a(bra) %b(reg)
00000000000aaaaa000000bbbbb00000
//branches forwards or backwards a signed ammount

%a(bra)i %b(immediate)
bbbbbbbbbbbaaaaa100000bbbbb00000


store %a(reg), %b(reg)
0000000000010001000000aaaaabbbbb

storei %a(immediate), %b(reg)
aaaaaaaaaaa10001100000aaaaabbbbb

//cache loads use pointer as where to load or store from/to, and rs1/imm as where to put it in cache
cache %a(reg)
0000000000010010000000aaaaa00000

cachei %a(immediate)
aaaaaaaaaaa10010000000aaaaa00000

shovel %a(reg)
0000000000010011000000aaaaa00000

shoveli %a(immediate)
aaaaaaaaaaa10011000000aaaaa00000

cmp %a(reg),%b(reg)
00000000000101000aaaaabbbbb00000

cmpi %a(reg),%b(immediate)
bbbbbbbbbbb101001aaaaabbbbb00000

call 
00000000000101010000000000000000

ret
00000000000101100000000000000000

inte %a(reg), %b(reg)
00000000000101110aaaaabbbbb00000

intei %a(reg), %b(immediate)
bbbbbbbbbbb101111aaaaabbbbb00000
