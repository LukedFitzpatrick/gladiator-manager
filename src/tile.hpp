#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>

class Tile {
public:
  // position/type
  Tile(int x, int y, int tileType);

  void render(SDL_Rect& camera);

  int getType();
  SDL_Rect getBox();

private:
  // collision box
  SDL_Rect box;
  int type;
};
