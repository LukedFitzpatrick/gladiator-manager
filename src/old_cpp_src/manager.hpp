#ifndef MANAGER_HPP
#define MANAGER_HPP
#include <list>
#include "gladiator.hpp"

using namespace std;

class Manager {
private:
  list<Gladiator> gladList;

public:
  void addGladiator(Gladiator g);
};

#endif
