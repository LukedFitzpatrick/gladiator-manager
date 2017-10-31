#ifndef INPUTOBJECT_H
#define INPUTOBJECT_H

#include <iostream>
#include <map>
#include "command.hpp"
using namespace std;



// an object passed to the game backend containing information about a user input
class InputObject {
private:
  string value;
  Command command;
  map<string, Command> valueCommandMap;
  
public:
  InputObject(string v, map<string, Command> vcMap);
  string getValue();
  void setValue(string v);
  Command getCommand();
};



#endif
