#ifndef GAMEDRIVER_HPP
#define GAMEDRIVER_HPP

#include "iodriver.hpp"

class GameDriver {
private:
  IODriver io;

public:
  GameDriver(const IODriver& ioDriver);
  void runGame();

};

#endif
