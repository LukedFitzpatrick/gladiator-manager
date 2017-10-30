#include <iostream>
#include <random>
#include "gamedriver.hpp"
#include "iodriver.hpp"
#include "manager.hpp"
#include "rng.hpp"
#define VERSION "0.01"


using namespace std;


mt19937 rng;

int main() {
  //rng(time(0));

  rng = mt19937(time(0));
  

  cout<<"== Gladiator Manager Version " << VERSION << " ==" << endl;

  // setup the input/output driver
  IODriver io;

  // the manager (load this in from save file eventually)
  Manager m;
  
  // setup the game backend
  GameDriver g(io, m);

  g.runGame();

}
