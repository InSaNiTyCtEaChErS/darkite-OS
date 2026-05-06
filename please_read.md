# assembly and implementation documentation

### definitions:

Branch: a RELATIVE jump.

.
### Quirks/features:

interrupts use a 4 bit value to decide where to go. refer to **name and value** for this information.

any instruction with a greater than 32 "immediate" without the immediate bit set raises a 0 value interrupt.

this is to jump back to a safe location on hitting garbage data. there is a 1 in 2 chance this works per instruction.

.

immediates are always sign extended from 11 or 21 bits to 32 bits

no paging, cache is one contiguous memory block

PC is 16-bit and counts by four.
branches go by instruction, with current instruction included for backwards branches

.
### modes

there are two different operating modes.

USER MODE: restricted to ALU, branches, and other basic instructions. check isa.spec for more info. cannot load and store to/from cache or branch to the lower half of cache (kernel space)

KERNEL MODE: allowed to use any instruction.
.
### interrupts

Interrupts jump to a manually set address, unique to each of the 16 interrupts.
these addresses can only be set in kernel mode.

interrupts also set the special INTE register which can be read from with a READ instruction.

### name and value
| name | value | info |
| ---- | ----- | ----------------- |
| invalid inst | -1 | invalid instruction interrupt |
| cs | 1 | sets the previous context value. return to go back to the last used context |
| unused | 2 | unused |
| unused | 3 | unused |
| keyboard | 4 | sets the inte register to the key pressed |
| reserved | 5-15 | RESERVED. DO NOT USE. |
    

.
### flags

refer to **memory map.md** and **special registers**

.
### branch prediction

branches are always predicted taken, unless the hint bit (rs2's least significant bit) is set. branches also allow linking by writing to any register except zr (this is how i acheive BAL opcodes)

### pipeline

pipeline depth is 3.

pipeline stages are: 

    writeback+fetch from cache
    decode&load registers
    execute and store to temp
.
### Registers

32x 32 bit wide registers. zero register is named as ZR.

r28 is also known as SP

r29/30 are general purpose pointer registers

r31 is also known as flags.

### flags

flags (flags register) are like this:

    0: carry
    1: eq
    2: low
    3: less (Signed)
    

.
### special registers 
(inacessible by instructions directly except where needed for the instruction to function):

    interrupt registers:
        16x 16 bit interrupt address registers.


### Instruction set

check isa.spec (instruction specifications in plaintext format. might be a little confusing, but should be readable.)
    

