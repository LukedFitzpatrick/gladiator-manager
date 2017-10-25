#include <iostream>
#include "iodriver.hpp"

using namespace std;

// if you ever add graphics, change output library etc. just need to
// change the implementation of this class

IODriver::IODriver() {
}


void IODriver::display(OutputObject o) {
  cout<<o.getValue()<<endl;
}


InputObject IODriver::getInput() {
  string input;
  getline(cin, input);
  return InputObject(input);
}
