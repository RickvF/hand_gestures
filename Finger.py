from FingerGesture import FingerGesture
from Gesture import Gesture

class Finger():
    def __init__(self, startIndex, landmarks, isThumb=False):
        #bottom landmark of a finger
        self.startIndex = startIndex
        #amount of landmarks per finger
        self.amountFingerPoints = 4
        #is the finger a thumb
        self.isThumb = isThumb
        #list of the landmarks for a finger
        self.landmarks = landmarks
        #list of gestures to detect for a single finger
        self.gestureList = []

        #subscribe to the finger gestures
        self.setupGesture()
    
    
    #Function to detect if a function is open (finger pointed to the sky)
    def isOpen(self):
        if(not self.isThumb): #when not a thumb than position top landmark of the finger need to be less than position lower landmark on the finger (position less means higher in the sky)
            if(self.landmarks[self.startIndex + 3][2] < self.landmarks[self.startIndex + 1][2]):
                return True
            else:
                return False
        else: #finger is a thump. Check how thumb is positioned on the left of right of the hand
            if(self.landmarks[6][1] > self.landmarks[18][1]):
                if(self.landmarks[self.startIndex + 3][1] > self.landmarks[self.startIndex + 1][1]):
                    return True
                else:
                    return False
            else:
                if(self.landmarks[self.startIndex + 3][1] < self.landmarks[self.startIndex + 1][1]):
                    return True
                else:
                    return False
    
    
    #Subsciption function for gestures on a single finger
    def setupGesture(self):
        self.gestureList = []        
        return self
    

    def getLandMark(self, number):
        return self.landmarks[self.startIndex + number]