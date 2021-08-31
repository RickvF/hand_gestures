from Finger import Finger

class Hand():
    def __init__(self, landmarks, isLeftHand=True):
        self.isLeftHand = isLeftHand
        self.landmarks = landmarks
        
        self.fingers = []
        for id, lm in enumerate(self.landmarks):
            if(((id-1) % 4) == 0):  
                if(id == 1):
                    self.fingers.append(Finger(id, self.landmarks, True))      
                else:
                    self.fingers.append(Finger(id, self.landmarks))   