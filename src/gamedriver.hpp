#ifndef GAMEDRIVER_HPP
#define GAMEDRIVER_HPP

#include "iodriver.hpp"
#include "manager.hpp"

class GameDriver {
private:
  IODriver io;
  Manager manager;
  
public:
  GameDriver(const IODriver& ioDriver, Manager& man);
  void runGame();

};

#endif
