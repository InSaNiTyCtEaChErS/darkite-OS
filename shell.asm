#CONST byte = r0
#CONST color = r1
#CONST index = r2
#ALIAS clear %a : sub %a,%a,%a
clear byte
clear index
addi index,32,index
<startlabel
jmp

;32 bytes offset from start of file
@______       ___      ______   __   __                          
@|  _  \     / _ \     |  _  |  | | / /  (%%%%%%) (%%%%%%) /%%%%)
@| | |  |   / / \ \    | |_| |  | |/ /     |%%|     |%%|   \%\   
@| | |  |  / /___\ \   | __  |  |   \      |%%|     |%%|    %%%%)
@| |_|  | / /     \ \  | | \ \  | |\ \     |%%|     |%%|   /%/   
@|_____/ /_/       \_\ |_|  \_\ |_| \_\  (%%%%%%)   |%%|   \%%%%)
@----------------------------------------------------------------
@start typing----meow                                            
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

;loop to display all 512 bytes of ascii data
    lp index
    addi index,1,index
    load byte
    <disp_ascii
    call
cmpi index,544
bgi -11


;spinning loop
