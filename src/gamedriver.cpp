#include "gamedriver.hpp"
#include "inputobject.hpp"
#include "outputobject.hpp"
#include "iodriver.hpp"
#include "command.hpp"
#include "gladiator.hpp"

using namespace std;

GameDriver::GameDriver(const IODriver& ioDriver, Manager& man) {
  this->io = ioDriver;
  this->manager = man;
}

void GameDriver::runGame() {
  while(true) {

    // get some input from io driver
    io.buildValueCommandMap();
    InputObject in = this->io.getInput();

    // process input
    string outputString;
    Command c = in.getCommand();

    switch(c) {
      case NEW_GLAD:
	{
	Gladiator g;
	this->manager.addGladiator(g);
	outputString = "Generated new gladiator: \n" + g.toString();
	}
      break;

      case SHOW_ALL_GLADS:
	outputString = "Show all glads requested";
      break;

      case HELP:
	outputString = io.getHelpString();
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

