class Converser:
    def __init__(self):
        # ... pass in particular types of converser
        pass

    def setAgent(self, a):
        self.agent = a
        
    def getDialogue(self, conversationState):
        # todo make this different for different people

        if conversationState == "HELLO":
            return self.agent.getName() + ": Hello!"
        elif conversationState == "TALK":
            return self.agent.getName() + ": I haven't got much to say!"
        elif conversationState == "RECRUIT":
            return self.agent.getName() + ": Recruit me?"
        elif conversationState == "FIGHT":
            return self.agent.getName() + ": Fight!"
        else:
            return self.agent.getName() + ": Luke Fitzpatrick doesn't know how to program!"
    
    
