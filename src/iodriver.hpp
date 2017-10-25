#ifndef IODRIVER_H
#define IODRIVER_H

#include "inputobject.hpp"
#include "outputobject.hpp"


class IODriver {
public: 
  IODriver();
  void display(OutputObject o);
  InputObject getInput();
};

#endif
