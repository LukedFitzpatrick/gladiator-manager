#ifndef IODRIVER_H
#define IODRIVER_H

#include "inputobject.hpp"
#include "outputobject.hpp"



class IODriver {
private:
  map<string, Command> vcMap;

public: 
  IODriver();

  // write an OutputObject to the screen
  void display(OutputObject o);

  // read in an InputObject and return it
  InputObject getInput();

  // set the input -> command mapping
  void buildValueCommandMap();

  // build a help string from the value -> command mapping
  string getHelpString();
};

#endif
