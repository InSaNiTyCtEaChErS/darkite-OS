#CONST byte = r0
#CONST index = r1
#ALIAS clear %a : sub %a,%a,%a
clear byte
clear index
addi index,32,index
<startlabel
jmp

;32 bytes offset from start of file
@______       ___      ______   __   __                          ;end of line strings, these are 64 chars each
@|  _  \     / _ \     |  _  |  | | / /  (%%%%%%) (%%%%%%) /%%%%);
@| | |  |   / / \ \    | |_| |  | |/ /     |%%|     |%%|   \%\   ;
@| | |  |  / /___\ \   | __  |  |   \      |%%|     |%%|    %%%%);
@| |_|  | / /     \ \  | | \ \  | |\ \     |%%|     |%%|   /%/   ;
@|_____/ /_/       \_\ |_|  \_\ |_| \_\  (%%%%%%)   |%%|   \%%%%);
@----------------------------------------------------------------;
@start typing----meow                                            ;

>startlabel
    lp index
    addi index,1,index
    load byte
    <serialio_byte
    call
cmpi index,544
bgi 6
<startlabel
jmp
