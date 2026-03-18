### every use of terabyte actually means tebibyte (1099511627776 bytes)

# 16 cpu control and status bytes

### byte 0: status and control LEDs
    bits:
        0: syson/off LED
        1: sysbooting LED
        2: error LED/invvalid instruction hit
        3: stack error LED/stack or fp overflow
        4: RAM issue LED
        5: GPU issue LED
        6: serial port unconnected LED
        7: pc increment LED 
        
### byte 1: FLAGS
    bits:
        0: carry flag
        1: equals flag
        2: lower flag(unsigned)
        3: less flag(signed)
        4: error flag
        5: interrupt enable flag
        6: constant 0
        7: constant 0
        
### bytes 2:7:
    relative pointer register, added to actual pointer

### zero bytes(for now) 8:15

# inputs and outputs

### serial i/o
    port 0: 7 bits of data
        TODO: DECIDE ORDER

# 128:130 terabytes: HDD/SSD 0
### all following blocks up to 256 terabytes are the same structure, just different drives. yes, we have a hard cap of two terabyte drives

