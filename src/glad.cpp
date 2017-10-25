#include <iostream>
#include "gamedriver.hpp"
#include "iodriver.hpp"

#define VERSION "0.01"


using namespace std;




int main() {
  cout<<"== Gladiator Manager Version " << VERSION << " ==" << endl;

  // setup the input/output driver
  IODriver io;

  // setup the game backend
  GameDriver g(io);

  g.runGame();

}
