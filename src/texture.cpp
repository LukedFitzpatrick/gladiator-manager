#include "texture.hpp"

using namespace std;

Texture::Texture(SDL_Renderer* r) {
  renderer = r;
  mTexture = NULL;
  width = 0;
  height = 0;
}

Texture::~Texture() {
  free();
}

bool Texture::loadFromFile(std::string path) {
  // get rid of preexisting texture
  free();

  // the final texture
  SDL_Texture* newTexture = NULL;

  // load image at specified path
  SDL_Surface* loadedSurface = IMG_Load(path.c_str());

  if(loadedSurface == NULL) {
    cout<< "Texture.cpp: Unable to load image " << path.c_str() << " " << IMG_GetError() << endl;
  }
  else {
    // color key image
    SDL_SetColorKey(loadedSurface, SDL_TRUE, SDL_MapRGB(loadedSurface->format, 0, 0xFF, 0xFF));

    // create texture from surface pixels
    newTexture = SDL_CreateTextureFromSurface(renderer, loadedSurface);
    if(newTexture == NULL) {
      cout <<"Texture.cpp: Unable to create texture " << path.c_str() << " " << SDL_GetError() << endl;
    }
    else {
      width = loadedSurface->w;
      height = loadedSurface->h;
    }

    // free loaded surface
    SDL_FreeSurface(loadedSurface);
  }

  // return success/failure
  mTexture = newTexture;
  return mTexture != NULL;
}


void Texture::free() {
  // free texture if it exists
  if(mTexture != NULL) {
    SDL_DestroyTexture(mTexture);
    mTexture = NULL;
    width = 0;
    height = 0;
  }
}

void Texture::setColor(Uint8 red, Uint8 green, Uint8 blue) {
  SDL_SetTextureColorMod(mTexture, red, green, blue);
}

void Texture::setBlendMode(SDL_BlendMode blending) {
  SDL_SetTextureBlendMode(mTexture, blending);
}
		
void Texture::setAlpha(Uint8 alpha) {
  SDL_SetTextureAlphaMod(mTexture, alpha);
}

void Texture::render(int x,
		     int y,
		     SDL_Rect* clip,
		     double angle,
		     SDL_Point* center,
		     SDL_RendererFlip flip) {

  // set rendering space and render to screen
  SDL_Rect renderQuad = {x, y, width, height};

  // set clip rendering dimensions
  if(clip != NULL) {
      renderQuad.w = clip->w;
      renderQuad.h = clip->h;
  }

  // render to screen
  SDL_RenderCopyEx(renderer, mTexture, clip, &renderQuad, angle, center, flip);
}

int Texture::getWidth() {
  return width;
}

int Texture::getHeight() {
  return height;
}
