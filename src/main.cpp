#include <SDL2/SDL.h>
#include <stdio.h>
#include <iostream>
#include <random>
#include "gamedriver.hpp"
#include "iodriver.hpp"
#include "manager.hpp"
#include "rng.hpp"

#define VERSION "0.01"


using namespace std;



const int TILE_SIZE = 32;

const int NUM_TILES = 16;

const int SCREEN_WIDTH = TILE_SIZE*NUM_TILES;
const int SCREEN_HEIGHT = TILE_SIZE*NUM_TILES;

mt19937 rng;


SDL_Window* initialiseSDLWindow() {
  SDL_Window* window = NULL;

  if(SDL_Init(SDL_INIT_VIDEO) < 0) {
    cout << "Couldn't launch SDL: " << SDL_GetError() << endl;
  }
  else {
    //Create window
    window = SDL_CreateWindow( "Gladiator Manager",
			       SDL_WINDOWPOS_UNDEFINED,
			       SDL_WINDOWPOS_UNDEFINED,
			       SCREEN_WIDTH,
			       SCREEN_HEIGHT,
			       SDL_WINDOW_SHOWN );
    if(window == NULL) {
      cout<< "Couldn't create a window: " << SDL_GetError() <<endl;
    }
  }

  return window;
}


int main( int argc, char* args[] )
{
  cout<<"== Gladiator Manager Version " << VERSION << " ==" << endl;

  // seed rng
  rng = mt19937(time(0));



  
  // setup the input/output driver
  IODriver io;

  // the manager (load this in from save file eventually)
  Manager m;
  
  // setup the game backend
  GameDriver g(io, m);

  //g.runGame(); 

  SDL_Window* window = initialiseSDLWindow();

  if(window != NULL) {

    // get the window's surface
    SDL_Surface* screenSurface = SDL_GetWindowSurface( window );
      
    // fill the surface with white
    SDL_FillRect( screenSurface, NULL, SDL_MapRGB( screenSurface->format, 0xFF, 0xFF, 0xFF ) );
			
    // update the window
    SDL_UpdateWindowSurface( window );

    // wait two seconds
    SDL_Delay( 2000 );

    //Destroy window
    SDL_DestroyWindow( window );
  }

  //Quit SDL subsystems
  SDL_Quit();

  return 0;
}
