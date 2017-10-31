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

  bool dead;
  
public:
  Gladiator();
  void generateSelf();
  string toString();
  bool isDead();

  int getSpeed();
  string fullName();
};

#endif
