

class Gesture():
    def __init__(self, description, condition):
        self.description = description
        self.condition = condition
    
    def getDescription(self):
        return self.description

    def isActive(self):
        return True if self.condition else False