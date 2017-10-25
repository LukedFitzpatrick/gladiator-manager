#include "gamedriver.hpp"
#include "inputobject.hpp"
#include "outputobject.hpp"
#include "iodriver.hpp"
#include "command.hpp"

using namespace std;

GameDriver::GameDriver(const IODriver& ioDriver) {
  this->io = ioDriver;
}

void GameDriver::runGame() {
  while(true) {

    // get some input from io driver
    InputObject in = this->io.getInput();

    // process input
    string outputString;
    Command c = in.getCommand();

    switch(c) {
      case NEW_GLAD:
	outputString = "New glad requested";
      break;

      case SHOW_ALL_GLADS:
	outputString = "Show all glads requested";
      break;

      default:
	outputString = "Huh?";
    }


    // build output
    OutputObject out(outputString);

    // send output to io driver
    this->io.display(out);
  }

}

