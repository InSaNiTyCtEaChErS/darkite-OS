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


int compile_check(u8 *pointer, u32 length){
    char start = *pointer;
    char next = *(pointer+1);

    switch (char){

        case 'a':
            if (next == 'w'){

            }else{
                
            }
        case 's':
            if (next == 'w'){
                
            }else{

            }
        case 'b':
            switch (next){
                case 'e': // branch equal

                
                case 'n': // branch not equal
 
                
                case 'a': // branch above equal
 
                
                case 'b': // branch below
 
                
                case 'l': // branch less 
 
                
                case 'g': // branch greater equal
 

                case 'r': // branch always

                
            }
            
    }


}   

int main(){
    char str[] = "jmp";
    char *string = str;
    compile_check(string,sizeof(string));
}
