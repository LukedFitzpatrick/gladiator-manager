#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include "gladiator.hpp"
#include "rng.hpp"
#include <random>


using namespace std;

Gladiator::Gladiator() {
  generateSelf();
}

void Gladiator::generateSelf() {

  int numNames = 192; // todo ugly
  
  // todo maybe move the file stuff so it only happens once
  // read in those names boi
  string names[numNames];
  ifstream file("data/names.txt");
  if(file.is_open()) {
    for(int i = 0; i < numNames; i++) {
      file >> names[i];
    }
  }

  // pick a first name and last name
  std::uniform_int_distribution<int> nameGen(0, numNames);
  this->firstName = names[nameGen(rng)];
  this->lastName = names[nameGen(rng)];

  // age
  std::uniform_int_distribution<int> ageGen(16, 65);
  this->age = ageGen(rng);
  
  // stats
  std::uniform_int_distribution<int> statGen(0, 100);
  this->attack = statGen(rng);
  this->defence = statGen(rng);
  this->speed = statGen(rng);  

  this->dead = false;
}


bool Gladiator::isDead() {
  return dead;
}

string Gladiator::toString() {
  return "**" + this->firstName + " " + this->lastName +
    " \t (" + to_string(this->age) + "): " +
    "A: " + to_string(this->attack) + ", " +
    "D: " + to_string(this->defence) + ", " +
    "S: " + to_string(this->speed) + " **\n";
}

string Gladiator::fullName() {
  return this->firstName + " " + this->lastName;
}

int Gladiator::getSpeed() {
  return speed;
}
