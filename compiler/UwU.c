#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>

typedef int8_t i8;
typedef int16_t i16;
typedef int32_t i32;
typedef int64_t i64;

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

#define RUN_TIME_NAME "portato"
#define BUILD_NUMBER "build 0\n"

#define SETTINGS_FILE "settings.txt"
#define COMPILER_FILE "encoder_v3.py"

    
int run(void){

    return 0;
}

int main(void) {

    printf("%s: booting\n%s", RUN_TIME_NAME, BUILD_NUMBER);
    
    // load settings
    char empty[32] = {};
    char window_width[32] = {};
    char window_height[32] = {};
    char working_file[32] = {};

    
    FILE *fptr;

    fptr = fopen(SETTINGS_FILE, "r");

    if(fptr == NULL) { // make sure settings exists
        printf("\e[31mERROR: SETTINGS.TXT MISSING. creating settings.txt\e[0m\n");
        fptr = fopen(SETTINGS_FILE,"w");
        fprintf(fptr,"size:\n640\n480\n\n\n");

    }
    fgets(empty,32,fptr);
    fgets(window_width,32,fptr);
    fgets(window_height,32,fptr);
    fgets(empty,32,fptr);
    fgets(working_file,32,fptr);

    printf("size:\n%s*\n%s",window_width,window_height);
    printf("last used file: %s\n",working_file);

    fclose(fptr);

    fptr = fopen(COMPILER_FILE, "r");
   
    if(fptr == NULL) { // make sure compiler exists
        printf("\e[31mERROR: COMPILER MISSING. please add the compiler file to the working directory.\e[0m\n");
        return -1;
    }
    fclose(fptr);

    fptr = fopen(working_file,"r");
    if (fptr == NULL){
        fptr = fopen(working_file,"w");
    }else{
        fclose(fptr);
    }

    bool default_state = false;
    if (working_file[0] = '\n'){
        default_state = true;
    }

    //window size is in window_width and window_height
    i32 ww = 0;
    i32 wh = 0;
    ww = strtol(window_width,NULL,0);
    wh = strtol(window_height,NULL,0);

    
//spawn window, borrow some code from the AI
    SDL_Window* window = NULL;
    SDL_Renderer* renderer = NULL;

    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        SDL_Log("Unable to initialize SDL: %s", SDL_GetError());
        return 1;
    }
     if (SDL_CreateWindowAndRenderer("An SDL3 window", ww, wh, 0, &window, &renderer) < 0) {
        SDL_Log("Window and renderer creation failed: %s", SDL_GetError());
        SDL_Quit();
        return 1;
    }
    
    SDL_Event event;
    bool quit = false;
    while (!quit) {
        // Poll for events
        while (SDL_PollEvent(&event)) {
            // Check for the quit event
            if (event.type == SDL_EVENT_QUIT) {
                quit = true;
            }
        }

        // --- Rendering code goes here ---
        // Set draw color to a light gray and clear the screen
        SDL_SetRenderDrawColor(renderer, 200, 200, 200, 255);
        SDL_RenderClear(renderer);
        
        // Update the screen with the cleared color
        SDL_RenderPresent(renderer);
    }


    // close out everything
    printf("exiting\n SAVING FILE");

    SDL_GetWindowSize(window, &ww, &wh);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    

    fptr = fopen(SETTINGS_FILE, "w");
        fprintf(fptr,"size:\n");
        snprintf(window_width,10,"%d",ww);
        fprintf(fptr,window_width);
        snprintf(window_height,10,"%d",wh);
        fprintf(fptr,window_height);
        fprintf(fptr,working_file);
    fclose(fptr);


    printf("\n\n\n");
}
