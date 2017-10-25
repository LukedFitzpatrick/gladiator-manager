#ifndef IODRIVER_H
#define IODRIVER_H

#include "inputobject.hpp"
#include "outputobject.hpp"



class IODriver {
private:
  map<string, Command> vcMap;

public: 
  IODriver();
  void display(OutputObject o);
  InputObject getInput();
  void buildValueCommandMap();
};

#endif
