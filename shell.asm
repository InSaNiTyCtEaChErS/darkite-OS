;header
brai 6
{3};tag count
{1};tag len 1
@os  ;tag 1
{1};tag len 2
@.exe;tag 2
{3};tag len 3
@immutable   ;tag 3
;end of file header

addi r7,32,r7
<startlabel
jmp

>code
@______       ___      ______   __   __                         
@|  _  \     / _ \     |  _  |  | | / / (%%%%%%) (%%%%%%) /%%%%)
@| | |  |   / / \ \    | |_| |  | |/ /    |%%|     |%%|   \%\   
@| | |  |  / /___\ \   | __  |  |   \     |%%|     |%%|    %%%%)
@| |_|  | / /     \ \  | | \ \  | |\ \    |%%|     |%%|   /%/   
@|_____/ /_/       \_\ |_|  \_\ |_| \_\ (%%%%%%)   |%%|   \%%%%)
@---------------------------------------------------------------
@start typing----meow                                           
;544 byte offset

#RESBY 2048;character buffer

>render

<<code, r5,r6
>render_loop

load r1
;add pointer by 1
addi r5,1,r5
awci r6,0,r6
addi r2,1,r2

andi r2,64,r4
addi r4,r3,r3
andi r2,63,r2

<disp_ascii
call
<render_loop
cmpi r3,40
bgei 1
jmp
ret



>startlabel



;spinning loop

cmpi r0,0
bei -2
cmpi r0,8
bnei 3


TODO: backspace character and character addition to temp buffer


<render
call

<startlabel
jmp

