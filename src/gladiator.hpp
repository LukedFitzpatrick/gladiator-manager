#ifndef GLADIATOR_HPP
#define GLADIATOR_HPP
#include <iostream>

using namespace std;

class Gladiator {
private:
  string firstName;
  string lastName;
  int age;

  
  // battle stats
  int attack;
  int defence;
  int speed;
  int intimidation;
  int mentalToughness;
  int xFactor;
  
public:
  Gladiator();
  void generateSelf();
  string toString();
};

#endif
