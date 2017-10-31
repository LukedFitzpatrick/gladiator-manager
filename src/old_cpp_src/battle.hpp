#ifndef BATTLE_HPP
#define BATTLE_HPP

#include <list>
#include <vector>
#include "gladiator.hpp"
#include "iodriver.hpp"
#include <iostream>

using namespace std;

class Battle {
private:
  list<Gladiator> aTeam;
  list<Gladiator> bTeam;

  void generateRandomTeams(int numATeam, int numBTeam);

public:
  Battle();
  
  string aTeamToString();
  string bTeamToString();
  string toString();

  void addGladiatorToATeam(Gladiator g);
  void addGladiatorToBTeam(Gladiator g);

  // returns true if A team wins, false if B team wins
  bool runBattle(IODriver io);
  
  void runTurn(IODriver io);

  bool isATeamAllDead();
  bool isBTeamAllDead();



};


#endif
