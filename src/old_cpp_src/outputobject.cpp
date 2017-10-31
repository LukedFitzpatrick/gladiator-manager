#include "outputobject.hpp"


OutputObject::OutputObject(string v) {
  this->value = v;
}

string OutputObject::getValue() {
  return this->value;
}

void OutputObject::setValue(string v) {
  this->value = v;
}
