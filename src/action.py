class Action:
    def __init__(self, name):
        self.name = name
        self.waitingForState = False
        self.waitingForInteraction = False

        self.changesState = False

        self.makesMessage = False
        self.messages = []

        self.changesObjectTiles = False
        self.changeObjectTiles = []

        self.changesObjectDialogue = False
        self.changeObjectDialogue = []


    # LITTLE TRIGGERS
    def setWhenInState(self, state):
        self.whenInState = state
        self.waitingForState = True

    def setWhenInteractWith(self, objectName):
        self.whenInteractWith = objectName
        self.waitingForInteraction = True

    # ACTIONS
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
        
    def triggeredBy(self, state, interactedWith):
        if(self.waitingForState and self.whenInState != state):
            return False
        
        # are we triggered by an interaction?
        if(self.waitingForInteraction and self.whenInteractWith == interactedWith):
            return True

        return False

    def performAction(self, level):
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
