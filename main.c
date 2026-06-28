#include "headers.h"
#include <SDL2/SDL_keycode.h>
#include <SDL2/SDL_timer.h>
#include <stdio.h>
#include <string.h>
#include <syscall.h>
int main(void){
    system("./venv311/bin/python app.py &");
    SDL_Init(SDL_INIT_AUDIO|SDL_INIT_VIDEO);
    IMG_Init(IMG_INIT_PNG);
    TTF_Init();
    SDL_Window* window=SDL_CreateWindow("fuckass drone",SDL_WINDOWPOS_CENTERED,SDL_WINDOWPOS_CENTERED,1280,720,SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer=SDL_CreateRenderer(window,-1,SDL_RENDERER_ACCELERATED);
    SDL_Surface* s=IMG_Load("assets/drone.png");
    SDL_Texture* drone=SDL_CreateTextureFromSurface(renderer,s);
    SDL_Surface* sm=IMG_Load("assets/dronestat.png");
    SDL_Texture* dronest=SDL_CreateTextureFromSurface(renderer,sm);
    SDL_Surface* bgs=IMG_Load("assets/epstein_island.png");
    SDL_Texture* bg=SDL_CreateTextureFromSurface(renderer,bgs);
    SDL_Rect bgr={0,0,1280,720};
    Uint32 currentime,lastime=0;
    int cur=0;
    int dir=0;//gonna use 0 for left and 1 for right 
    int frame_d=50;
    int px=300,py=300;
    FILE* file;
    
    bool running=true;
    SDL_Event event; //bitchass timing the mf wont start
    char state[100];
    while (running){
        file=fopen("state.txt","r");
        fscanf(file,"%s",state);
        if (strcmp(state,"down")==0){
            if(py<720){
                py+=2;
            }
        }else if (strcmp(state,"up")==0){
            if(py>0){
                py-=2;
            }

        }else if (strcmp(state,"left")==0){
            if(px<1280 && px>0){
                px-=2;
            }
            dir=0;
//here i was stuck for about 20 minutes just bcz i used =+ instead of -= .. bruh things be just overreacting walah
        }else if (strcmp(state,"right")==0){
            if(px<1280 && px>0){
                px+=2;
            }
            dir=1;
        }

        while(SDL_PollEvent(&event)){
            if (event.type==SDL_QUIT){
                running =false;

            }else if (event.type==SDL_KEYDOWN){
                SDL_KeyCode key=event.key.keysym.sym;
                if (key==SDLK_DOWN){
                    if(py<720){
                        py+=10;
                    }
                }else if (key==SDLK_UP){
                    if(py>0){
                        py-=10;
                    }

                }else if (key==SDLK_LEFT){
                    if(px<1280 && px>0){
                        px-=10;
                    }
                    dir=0;
//here i was stuck for about 20 minutes just bcz i used =+ instead of -= .. bruh things be just overreacting walah
                }else if (key==SDLK_RIGHT){
                    if(px<1280 && px>0){
                        px+=10;
                    }
                    dir=1;

                }

            }
        }
        
        currentime=SDL_GetTicks();
        if (currentime>lastime+frame_d){
            lastime=currentime;
            cur=(cur+1)%36;
        }
        
        SDL_SetRenderDrawColor(renderer,140,90,180,255);
        SDL_RenderClear(renderer);
        SDL_RenderCopy(renderer,bg,NULL,&bgr);
        animate(px,py,dir,drone,renderer,currentime,lastime,cur);
        
        SDL_RenderPresent(renderer);
        SDL_Delay(16);
    }
    TTF_Quit();
    IMG_Quit();
    SDL_Quit();


}