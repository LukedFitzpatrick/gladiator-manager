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
  this->intimidation = statGen(rng);
  this->mentalToughness = statGen(rng);
  this->xFactor = statGen(rng);
  
  
}

string Gladiator::toString() {
  return "== " + this->firstName + " " + this->lastName +
    " (" + to_string(this->age) + ") ==\n" +
    "  Attack: " + to_string(this->attack) + "\n" +
    "  Defence: " + to_string(this->defence) + "\n" +
     "  Speed: " + to_string(this->speed) + "\n" +
    "  Intimidation: " + to_string(this->intimidation) + "\n" +
  "  Mental Toughness: " + to_string(this->mentalToughness) + "\n" +
     "  X-Factor: " + to_string(this->xFactor) + "\n";
}
