#ifndef OUTPUTOBJECT_H
#define OUTPUTOBJECT_H


#include <iostream>
using namespace std;


// an object passed to the game frontend containing information about
// what to display
class OutputObject {
private:
  string value;

public:
  OutputObject(string v);
  string getValue();
  void setValue(string v);
};



#endif
