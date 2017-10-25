#ifndef INPUTOBJECT_H
#define INPUTOBJECT_H


#include <iostream>
using namespace std;


// an object passed to the game backend containing information about a user input
class InputObject {
private:
  string value;

public:
  InputObject(string v);
  string getValue();
  void setValue(string v);
};



#endif
