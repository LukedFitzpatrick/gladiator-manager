#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>

class Player {
public:

  // TODO change the player to be an image
  static const int DOT_WIDTH = 20;
  static const int DOT_HEIGHT = 20;

  // maximum axis velocity
  static const int DOT_VEL = 10;

  //Initializes the variables
  Player();

  // takes key presses and adjusts the player's velocity
  void handleEvent(SDL_Event& e);

  // moves the player and check collision against tiles
  void move(Tile *tiles[]);

  // centers the camera over the player
  void setCamera(SDL_Rect& camera);


  void render(SDL_Rect& camera);

private:
  // collision box
  SDL_Rect box;

  // velocity
  int xV, yV;
};
