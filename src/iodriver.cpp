#include <iostream>
#include "iodriver.hpp"
#include <string.h>
#include <vector>


using namespace std;

// if you ever add graphics, change output library etc. just need to
// change the implementation of this class

IODriver::IODriver() {
  this->buildValueCommandMap();
}


void IODriver::display(OutputObject o) {
  cout<<o.getValue()<<endl;
}


InputObject IODriver::getInput() {
  string input;
  getline(cin, input);
  return InputObject(input, this->vcMap);
}



// todo pass things in here to make it context sensitive
void IODriver::buildValueCommandMap() {
  map<string, Command> m;

  m["n"] = NEW_GLAD;
  m["s"] = SHOW_ALL_GLADS;
  m["h"] = HELP;

  
  this->vcMap = m;
}


string IODriver::getHelpString() {
  return "help not implemented yet";
}
