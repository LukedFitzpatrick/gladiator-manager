#include "gamedriver.hpp"
#include "inputobject.hpp"
#include "outputobject.hpp"
#include "iodriver.hpp"

using namespace std;

GameDriver::GameDriver(const IODriver& ioDriver) {
  this->io = ioDriver;
}

void GameDriver::runGame() {
  while(true) {

    // get some input from io driver
    InputObject in = this->io.getInput();


    // process input
    string outputString = in.getValue();
    

    // build output
    OutputObject out(outputString);

    // send output to io driver
    this->io.display(out);
  }
}
