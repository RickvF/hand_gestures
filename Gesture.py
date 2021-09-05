

class Gesture():
    def __init__(self, hand, description, condition):
        #Indentification of hand
        self.hand = hand
        #Identification of the gesture
        self.description = description
        #Condition what finger positions need to be to trigger the gesture
        self.condition = condition
    
    
    #Description to identify gesture
    def getDescription(self):
        return self.description

    
    #Check if the gesture is active
    def isActive(self):
        return True if self.condition else False