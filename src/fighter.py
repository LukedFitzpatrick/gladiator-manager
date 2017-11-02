class Fighter:
    def __init__(self, name, baseHealth, baseKnifeDamage):
        self.name = name
        self.baseHealth = baseHealth
        self.baseKnifeDamage = baseKnifeDamage
        self.currentHealth = baseHealth
        self.alive = True
        
    def dealDamage(self, damage):
        self.currentHealth -= damage
        print self.name + " took " + str(damage) + " damage, hp=" + str(self.currentHealth)
        if(self.currentHealth < 0):
            self.alive = False
            print self.name + " died."
    

    def getHealthPercent(self):
        return (self.currentHealth/self.baseHealth)*100
