#ifndef TEXTURE_HPP
#define TEXTURE_HPP

#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <stdio.h>
#include <string>
#include <fstream>
#include <iostream>



class Texture {
public:
  Texture(SDL_Renderer* r);
  
  ~Texture();

  bool loadFromFile(std::string path);

  // deallocates texture
  void free();

  // set color modulation
  void setColor(Uint8 red, Uint8 green, Uint8 blue);

  // set blending
  void setBlendMode(SDL_BlendMode blending);

  // set alpha modulation
  void setAlpha(Uint8 alpha);
		
  // render texture at given point
  void render(int x, int y,
	      SDL_Rect* clip = NULL,
	      double angle = 0.0,
	      SDL_Point* center = NULL,
	      SDL_RendererFlip flip = SDL_FLIP_NONE );

  // get image dimensions
  int getWidth();
  int getHeight();

private:
  // the actual hardware texture
  SDL_Texture* mTexture;

  // window renderer
  SDL_Renderer* renderer;

  // image dimensions
  int width;
  int height;
};

#endif
