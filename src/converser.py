class Converser:
    def __init__(self, tree):
        print tree
        self.tree = tree

    def setAgent(self, a):
        self.agent = a

    def setTree(self, tree):
        self.tree = tree
        
    def getDialogue(self, conversationState):
        # todo make this different for different people

        if(self.tree == "idiot"):
            if conversationState == "HELLO":
                return self.agent.getName() + ": Hello!"
            elif conversationState == "TALK":
                return self.agent.getName() + ": I haven't got much to say!"
            elif conversationState == "RECRUIT":
                return "GET_RECRUITED"
            elif conversationState == "FIGHT":
                return self.agent.getName() + ": I don't fight!"
            else:
                return self.agent.getName() + ": Luke Fitzpatrick doesn't know how to program!"
    
    
        if(self.tree == "ally"):
            if conversationState == "HELLO":
                return self.agent.getName() + ": We're going to make it to Rome one day!"
            elif conversationState == "TALK":
                return self.agent.getName() + ": What else is there to say?"
            elif conversationState == "RECRUIT":
                return self.agent.getName() + ": I'm already a recruit!"
            elif conversationState == "FIGHT":
                return self.agent.getName() + ": I don't fight friends!"
            else:
                return self.agent.getName() + ": Luke Fitzpatrick doesn't know how to program!"
            
