#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

typedef int8_t i8;
typedef int16_t i16;
typedef int32_t i32;
typedef int64_t i64;

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

#define FILE_TO_LOAD "/working_file.txt"
#define FILE_TO_WRITE "/runtime.txt"

int getreg(u8 *pointer){
    bool reg = false;
    bool quit = false;
    int regnum = 0;
    for (u8 i; i < 255; i++){
        if (*(pointer+i) == 'r'){
            reg = true;
            continue;
        }
        regnum = regnum*10;
        switch (*(pointer+i)) // translate characters into numbers
        {
            case '0': break;// too lazy to use strtol apparently
            case '1':regnum += 1;break;
            case '2':regnum += 2;break;
            case '3':regnum += 3;break;
            case '4':regnum += 4;break;
            case '5':regnum += 5;break;
            case '6':regnum += 6;break;
            case '7':regnum += 7;break;
            case '8':regnum += 8;break;
            case '9':regnum += 9;break;
            case ';':quit = true;break;
            case ',':quit = true;break;
            case '\0':quit = true;break;
            default:

        }
        if (quit == true){
            break;
        }
    }
    regnum = regnum / 10;

    return regnum;
}

int compile_check_line(u8 *pointer, u32 length){ // compile a line into data-------------------------------------------------------------------------------------------------------
    //find opcode
    char opcodes[32][3] = {"add","awc","sub","swc","nan","and","lsl","lsr","jum","bra","be ","bne","bl ","bge","bae","bb ","loa","sto","cmp","cal","ret","int","lui","unu"};
    bool inst = true;
    u8 opcode = -1;
    for (int i; i<32;i++){
        inst = true;
        if (*(pointer) != opcodes[i][0]){
            inst = false;
        }
        if (*(pointer+1) != opcodes[i][1]){
            inst = false;
        }
        if (*(pointer+2) != opcodes[i][2]){
            inst = false;
        }
        if (inst == true){
            opcode = i;
            break;
        }
    }
    if (inst == false){
        return -1; // invalid opcode
    }
    
    // find space
    int space = -1;
    bool end = false;
    for (int i; i<length;i++){
        if (*(pointer+i) == ' '){
            space = i;
        }
        if (*(pointer+i) == '\n'){
            space = i;
            end = true;
        }
    }
    if (end == true){
        //encode zero argument instructions
        return(opcode<<16);
    }

}   

int compile(u8 *pointer, u32 length){ // compile a pointer and length into instruction code-----------------------------------------------------------------------------------
    char line[64] = {};
    u8 index = 0;

    for (int i; i<length; i++){
        if (*(pointer+i) == '\n'){
            //pad out line with spaces
            for (int j = index; j<64;j++){
                line[j] = ' ';
            }
            //compile line
            if (line[0] == ';'){
                continue;
            }


        }else{
            line[index] = *(pointer+i);
            index ++;
        }
    }


    

    return 0;
}


int main(void){
    
}
