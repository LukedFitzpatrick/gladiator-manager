#include "battle.hpp"

using namespace std;


Battle::Battle() {
  cout<<"Setting up battle"<<endl;
  generateRandomTeams(3, 3);
}


bool Battle::isATeamAllDead() {
  for(Gladiator g : aTeam) {
    if(!g.isDead()) {
      return false;
    }
  }
  return true;
}

bool Battle::isBTeamAllDead() {
  for(Gladiator g : bTeam) {
    if(!g.isDead()) {
      return false;
    }
  }
  return true;
}


void Battle::runTurn(IODriver io) {

  // run each gladiator's turn in order
  std::vector<Gladiator*> allGlads;

  for(Gladiator g : aTeam) {
    cout << "RunTurnA : " << (&g)->fullName() << endl;
    allGlads.push_back(&g);
  }
  for(Gladiator g : bTeam) {
    cout << "RunTurnB : " << (&g)->fullName() << endl;
    allGlads.push_back(&g);
  }

  //allGlads.sort([](Gladiator* lhs, Gladiator* rhs) {return lhs->getSpeed() > rhs->getSpeed();});

  for(int i = 0; i<6; i++) {
    cout<<allGlads[i]->fullName()<<endl;
  }
    
}

bool Battle::runBattle(IODriver io) {
  io.display(this->toString());

  int turnCount = 0;
  
  while(turnCount < 1 && !isATeamAllDead() && !isBTeamAllDead()) {
    // display turn count message
    string turnCountMessage = "\n== Turn #" + to_string(turnCount++) + " ==";
    io.display(turnCountMessage);

    // run the turn
    runTurn(io);
  }


  
  if(isATeamAllDead() && isBTeamAllDead()) {
    io.display((string) "DRAW: Unhandled, shouldn't have happened");
  }

  // if they're all dead, A team wins, otherwise A team loses
  return isBTeamAllDead();
}


void Battle::generateRandomTeams(int numATeam, int numBTeam) {
  for(int i = 0; i<numATeam; i++) {
    Gladiator g;
    addGladiatorToATeam(g);
  }
  for(int i = 0; i<numBTeam; i++) {
    Gladiator g;
    addGladiatorToBTeam(g);
  }  
}

void Battle::addGladiatorToATeam(Gladiator g) {
  //cout << "Adding glad: " << g.fullName() << endl;
  aTeam.push_back(g);
}


void Battle::addGladiatorToBTeam(Gladiator g) {
  bTeam.push_back(g);
}



string Battle::aTeamToString() {
  string str = "";
  for (Gladiator g : aTeam) {
    str += "\t" + g.toString();
  }
  return str;
}

string Battle::bTeamToString() {
  string str = "";
  for (Gladiator g : bTeam) {
    str += "\t" + g.toString();
  }
  return str;
}

string Battle::toString() {
  return "=== A TEAM ===\n" + aTeamToString() + "\n" +
    "=== B TEAM === \n" + bTeamToString();
}
