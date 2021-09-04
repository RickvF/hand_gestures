from Finger import Finger
from HandGesture import HandGesture
from Gesture import Gesture

#X and Y different between point finger and thumb for OK sign
OK_FINGER_DISTANCE = 50

class Hand():
    def __init__(self, landmarks, isLeftHand=True):
        #Is the hand a left hand
        self.isLeftHand = isLeftHand
        #list of handmarks of all fingers of the hand
        self.landmarks = landmarks
        #Subscription list of all gestures for the hand
        self.gestureList = []
        
        #Register all fingers
        self.fingers = []
        for id, lm in enumerate(self.landmarks):
            if(((id-1) % 4) == 0):  #go over it per 4 landmarks to mark a finger
                if(id == 1): #Finger is a thumb
                    self.fingers.append(Finger(id, self.landmarks, True))      
                else:
                    self.fingers.append(Finger(id, self.landmarks))   
        
        #Register all gestures for the hand
        self.setupGesture()
    
    
    #Function to showcase if it is left of right hand
    def getHandDescription(self):
        if(self.isLeftHand):
            return "Left"
        else:
            return "Right"

    
    #detect which gesture is active
    def detectGesture(self):
        for i, gesture in enumerate(self.gestureList):
            if(gesture.isActive()):
                print(gesture.getDescription())
                break

    
    #Subsciption function for gestures on a single hand
    def setupGesture(self):
        self.gestureList = []

        #Thumb up
        self.gestureList.append(HandGesture(self.getHandDescription() +  " Thumb up", True if (self.fingers[0].getLandMark(3)[2] < self.fingers[0].getLandMark(1)[2] and self.fingers[1].getLandMark(3)[2] < self.fingers[2].getLandMark(3)[2] and self.fingers[2].getLandMark(3)[2] < self.fingers[3].getLandMark(3)[2] and self.fingers[0].getLandMark(3)[2] < self.fingers[2].getLandMark(1)[2]) else False))
        #Thumb down
        self.gestureList.append(HandGesture(self.getHandDescription() +  " Thumb down", True if (self.fingers[0].getLandMark(3)[2] > self.fingers[0].getLandMark(1)[2] and self.fingers[1].getLandMark(3)[2] > self.fingers[2].getLandMark(3)[2] and self.fingers[2].getLandMark(3)[2] > self.fingers[3].getLandMark(3)[2] and self.fingers[0].getLandMark(3)[2] > self.fingers[2].getLandMark(1)[2]) else False))
        #All fingers up
        self.gestureList.append(HandGesture(self.getHandDescription() +  " hand open", True if (self.fingers[0].isOpen() and self.fingers[1].isOpen() and self.fingers[2].isOpen() and self.fingers[3].isOpen() and self.fingers[4].isOpen()) else False))
        #Hand closed
        self.gestureList.append(HandGesture(self.getHandDescription() +  " hand closed", True if (not self.fingers[0].isOpen() and not self.fingers[1].isOpen() and not self.fingers[2].isOpen() and not self.fingers[3].isOpen() and not self.fingers[4].isOpen()) else False))
        #OK sign
        self.gestureList.append(HandGesture(self.getHandDescription() +  " OK sign", True if (abs(self.fingers[0].getLandMark(3)[1] - self.fingers[1].getLandMark(3)[1]) < OK_FINGER_DISTANCE and abs(self.fingers[0].getLandMark(3)[2] - self.fingers[1].getLandMark(3)[2]) < OK_FINGER_DISTANCE and self.fingers[2].isOpen() and self.fingers[3].isOpen() and self.fingers[4].isOpen()) else False))
        

        #Count amount fingers 
        numberFinger = 0
        for j, finger in enumerate(self.fingers):
            if(finger.isOpen()):
                numberFinger = numberFinger + 1
        # 4 finger
        self.gestureList.append(HandGesture(self.getHandDescription() +  " 4 fingers", True if (numberFinger == 4) else False))
        # 3 fingers
        self.gestureList.append(HandGesture(self.getHandDescription() +  " 3 fingers", True if (numberFinger == 3) else False))
        # 2 fingers
        self.gestureList.append(HandGesture(self.getHandDescription() +  " 2 fingers", True if (numberFinger == 2) else False))
        # 1 finger
        self.gestureList.append(HandGesture(self.getHandDescription() +  " 1 fingers", True if (numberFinger == 1) else False))  

        return self