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


#CONST byte = r0
#CONST color = r1
#CONST index = r2
#ALIAS clear %a : sub %a,%a,%a
clear byte
clear index
addi index,32,index
<startlabel
jmp

>code
@______       ___      ______   __   __                          ;
@|  _  \     / _ \     |  _  |  | | / /  (%%%%%%) (%%%%%%) /%%%%);
@| | |  |   / / \ \    | |_| |  | |/ /     |%%|     |%%|   \%\   ;
@| | |  |  / /___\ \   | __  |  |   \      |%%|     |%%|    %%%%);
@| |_|  | / /     \ \  | | \ \  | |\ \     |%%|     |%%|   /%/   ;
@|_____/ /_/       \_\ |_|  \_\ |_| \_\  (%%%%%%)   |%%|   \%%%%);
@----------------------------------------------------------------;
@start typing----meow                                            ;
;544 byte offset
;alpha (higher = more transparent
{0}
;red
{255}
;green
{0}
;blue
{255}

>startlabel

;setup color
clear r4
addi r4,544
lp r4
load r3
or r3,r1,r1
addi r4,1,r4
lp r4
load r3
or r3,r1,r1
addi r4,1,r4
lp r4
load r3
or r3,r1,r1
addi r4,1,r4
lp r4
load r3
or r3,r1,r1
addi r4,1,r4
<color_code

;loop to display all 512 bytes of ascii data
    lp index
    addi index,1,index
    load byte
    <disp_ascii
    call
cmpi index,544
bgi -11


;spinning loop
