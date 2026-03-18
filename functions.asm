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
push r2
push r3
    ;display an ASCII character

pull r2
pull r3
ret

>serial_color_code
push r0
    ;output an ANSI color code over the serial port

pull r0
ret
