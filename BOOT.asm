brai 19 ;4 byte skipped space at begining of file
{3};3 tags
{1};tag length 1(4 bytes)
@os  ;tag
{1};tag length 1(4 bytes)
@.exe;tag
{3};tag length 3(12 bytes)
@immutable   ;tag, comment used for proper parsing
@    ;padding space
;code goes here
;file table goes on byte 256 (aka after 64 instructions)
push r1
key r1 
cmpi r1,-1
bnei 6
<INVALID_ISNT
jmp
<interrupt_matrix
jmp
printcount

