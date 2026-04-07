#CONST x = r1
#CONST y = r2
#CONST offset = r3
#CONST index = r4
#CONST scroll = r5
#CONST temp = r6
#MACRO clear %a = sub %a,%a,%a



<code
jmp

>__terminal_load_text
@______       ___      ______   __   __                         ;
@|  _  \     / _ \     |  _  |  | | / / (%%%%%%) (%%%%%%) /%%%%|;
@| | |  |   / / \ \    | |_| |  | |/ /    |%%|     |%%|   \%\   ;
@| | |  |  / /___\ \   | __  |  |   \     |%%|     |%%|    %%%%|;
@| |_|  | / /     \ \  | | \ \  | |\ \    |%%|     |%%|   /%/   ;
@|_____/ /_/       \_\ |_|  \_\ |_| \_\ (%%%%%%)   |%%|   \%%%%|;
@---------------------------------------------------------------;
@start typing----meow                                           ;
>__character_buffer
resby 8192;reserve 128 lines of space

>framebuffer
#RESBY 2048;reserve enough space for a 64*32 terminal

>__render_loop

;make x and y into offset
roli y,6,offset
or offset,x,offset
;we now have offset containing the bits: yyyyyyyyyyyyyyyyyyyyyyyyyyxxxxxx
;add the offset of the raw text data
<__terminal_load_text
addi r29,offset,offset
;offset is where we read from, index is the limit to stop printing
addi offset,512,index


;incrememt x
addi x,1,x
andi x,64,temp
rori temp,6,temp
addi y,temp,y


>__boot_code
























>__font
