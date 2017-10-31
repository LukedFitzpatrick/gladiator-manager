#include "inputobject.hpp"

InputObject::InputObject(string v, map<string, Command> vcMap) {
  //buildValueCommandMap();
  this->value = v;
  this->valueCommandMap = vcMap;

  if(vcMap.count(value)) {
    this->command = this->valueCommandMap[v];
  }
  else {
    this->command = UNKNOWN;
  }
}

string InputObject::getValue() {
  return this->value;
}

void InputObject::setValue(string v) {
  this->value = v;
}

Command InputObject::getCommand() {
  return this->command;
}
