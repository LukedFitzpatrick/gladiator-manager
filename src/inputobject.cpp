#include "inputobject.hpp"


InputObject::InputObject(string v) {
  this->value = v;
}

string InputObject::getValue() {
  return this->value;
}

void InputObject::setValue(string v) {
  this->value = v;
}

