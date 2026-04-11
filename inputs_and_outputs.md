data signals:
clock:
cpu clock. doesn't have a decided frequency yet
reset:
resets the cpu and registers to all zeroes, including the internal cache.

byte 0:
cpu in. takes in the current instruction byte

byte 1:
cpu out. outputs the current 32 bit pc address (over those same four cycles) for the next load

bidirectional byte:
bit 0:
status LED
bit 1: serial i/o 
bit 2: vga 1
bit 3: vga clock
bit 4-7: UNASSIGNED
