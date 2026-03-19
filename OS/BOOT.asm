brai 6 ;4 byte skipped space at begining of file
{3};3 tags
{1};tag length 1(4 bytes)
@os  ;tag
{1};tag length 1(4 bytes)
@.exe;tag
{3};tag length 3(12 bytes)
@immutable   ;tag, comment used for proper parsing
brai 15
;code goes here
;file table goes on byte 128 (aka after 32 instructions)
key r0 
cmpi r0,-1
bnei 6
<INVALID_ISNT
jmp
<interrupt_matrix
jmp
<terminal
jmp
nop
nop
{255};invalid instruction to trigger interrupt if it gets this far
{255}
{255}
{255}
printcount


resby 2048
