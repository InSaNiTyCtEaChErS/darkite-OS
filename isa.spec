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

bra
bra 01001
be  01010
bne 01011
bl  01100
bg  01101
bb  01110
ba  01111



[instructions]

//alu ------------------------------------------------------
%a(alu) %b(reg), %c(reg), %d(reg)
00000000000aaaaa0bbbbbcccccddddd

%a(alu)i %b(reg), %c(immediate), %d(reg)
cccccccccccaaaaa1bbbbbcccccddddd

//pc operations ---------------------------------------------
jump
00000000000010000000000000000000

%a(bra) %b(reg)
00000000000aaaaa000000bbbbb00000

%a(bra)i %b(immediate)
bbbbbbbbbbbaaaaa100000bbbbb00000

load %a(reg), %b(reg)
0000000000010000000000aaaaabbbbb

//memory operations ------------------------------------------
loadi %a(immediate), %b(reg)
aaaaaaaaaaa10000000000aaaaabbbbb

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

//special
call 
00000000000101010000000000000000

ret
00000000000101100000000000000000

inte %a(reg), %b(reg)
00000000000101110aaaaabbbbb00000

intei %a(reg), %b(immediate)
bbbbbbbbbbb101111aaaaabbbbb00000
