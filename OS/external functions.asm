{0}
{0}
{0}
{0}
{3};3 tags
{1};tag length 1(4 bytes)
@os  ;tag
{1};tag length 1(4 bytes)
@.exe;tag
{3};tag length 3(12 bytes)
@immutable   ;tag, comment used for proper parsing

;summary: 

;print_string
;display_pixel
;use_port
:spawn_terminal
;resize_terminal
;kill_terminal






>print_string
;takes a string to print to terminal n
;pointer:r1-2
;length: r3
;terminal to print to: r4


ret

>display_pixel
;takes an x and a y index to display at, and a pixel color
;x: r1
;y: r2
;color(32 bit): r3


ret

>use_port
;takes a port to use, pointer to data, and a data length
;pointer: r1-2
;length: r3
;port to use: r4


ret

>spawn_terminal
;spawn a terminal at an x,y position with width and height w,z
;x-y is r1-2
;width is r3
;height is r4


ret

>resize_terminal
;resize terminal id
;id is r1
;width is r3
;height is r4


ret

>kill_terminal
;kill terminal id
;id is r1

ret
