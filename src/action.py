class Action:
    def __init__(self, name):
        self.name = name
        self.waitingForState = False
        self.waitingForLightState = False
        self.waitingForInteraction = False
        self.whenInteractWith = []

        self.setsObjective = False
        self.changesState = False
        self.makesMessage = False
        self.messages = []
        self.changesObjectTiles = False
        self.changeObjectTiles = []
        self.changesObjectDialogue = False
        self.changeObjectDialogue = []
        self.changesLevel = False
        self.invertLighting = False
        self.setLighting = False
        self.changesLightState = False
        self.getsTorch = False
        
    # LITTLE TRIGGERS
    def setWhenInState(self, state):
        self.whenInState = state
        self.waitingForState = True

    def setWhenInLightState(self, state):
        self.whenInLightState = state
        self.waitingForLightState = True
        
    def addWhenInteractWith(self, objectName):
        self.whenInteractWith.append(objectName)
        self.waitingForInteraction = True

    # ACTIONS
    def setGetTorch(self, torch):
        self.getsTorch = True
    
    def setInvertLighting(self, i):
        self.invertLighting = i

    def setLight(self, r, g, b):
        self.setLighting = True
        self.light = (r, g, b)

    def setChangeLightState(self, state):
        self.changesLightState = True
        self.changeLightState = state
        
    def setChangeStateTo(self, state):
        self.changesStateTo = state
        self.changesState = True

    def addMessage(self, message):
        self.messages.append(message)
        self.makesMessage = True


    def addChangeObjectTile(self, objectName, newTileId):
        self.changesObjectTiles = True
        self.changeObjectTiles.append((objectName, newTileId))


    def addChangeObjectDialogue(self, objectName, newDialogue):
        self.changesObjectDialogue = True
        self.changeObjectDialogue.append((objectName, newDialogue))

    def setChangeLevel(self, level):
        self.changesLevel = True
        self.changeLevelTo = level


    def setObjective(self, objective):
        self.setsObjective = True
        self.objective = objective
        
    def triggeredBy(self, state, lightState, interactedWith):
        if(self.waitingForState and self.whenInState != state):
            return False
        
        if(self.waitingForLightState and self.whenInLightState != lightState):
            return False
        
        # are we triggered by an interaction?
        if self.waitingForInteraction:
            for i in self.whenInteractWith:
                if i == interactedWith:
                    return True
            return False

        return True

    
    def performAction(self, level):
        print "action " + self.name + " triggered!"
        if(self.changesLevel):
            level.changeLevel(self.changeLevelTo)
        
        if(self.changesState):
            level.changeState(self.changesStateTo)

        if(self.makesMessage):
            for m in self.messages:
                level.addMessage(m)

        if(self.changesObjectTiles):
            for e in self.changeObjectTiles:
                (objName, newTile) = e
                level.changeObjectTile(objName, newTile)

        if(self.changesObjectDialogue):
            for e in self.changeObjectDialogue:
                (objName, newDialogue) = e
                level.changeObjectDialogue(objName, newDialogue)

        if(self.setsObjective):
            level.setObjective(self.objective)

        if(self.invertLighting):
            level.ambientLight = map(lambda x: 255-x, level.ambientLight)

        if(self.setLighting):
            level.ambientLight = self.light

        if(self.changesLightState):
            level.lightState = self.changeLightState

        if(self.getsTorch):
            level.setTorch(True)
