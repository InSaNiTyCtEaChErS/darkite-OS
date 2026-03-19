brai 6 ;4 byte skipped space at begining of file
{3};3 tags
{1};tag length 1(4 bytes)
@func;tag
{1};tag length 1(4 bytes)
@.exe;tag
{3};tag length 3(12 bytes)
@immutable   ;tag, comment used for proper parsing



>INVALID_INST
;handle invalid instructions on a core
sub r0,r0,r0
subi r0,1,r0

ret

>interrupt_matrix
;handle sending interrupts to in-focus process


ret

>serialio_byte
push r1
    ;export a byte through the serial input/output

pull r1
ret

>disp_ascii
push r3
push r4
    ;display an ASCII character at a specified x and y in the framebuffer
    <<framebuffer r3,r4 ;load framebuffer using registers 3 and 4
    ;multiply x and y position to get framebuffer index, then add to offset
    TODO: do above

pull r4
pull r2
ret

>serial_color_code
push r0
    ;output an ANSI color code over the serial port

pull r0
ret




>framebuffer
#RESBY 16200 ;ASCII framebuffer size, each char is one byte, plus one for color
