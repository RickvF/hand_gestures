from Finger import Finger
from HandGesture import HandGesture
from Gesture import Gesture
from enum import Enum

class GestureDescription(Enum):
    NONE = -1
    THUMB_UP = 0
    THUMB_DOWN = 1
    HAND_OPEN = 2
    HAND_CLOSED = 3
    OK_SIGN = 4
    FOUR_FINGERS = 5
    THREE_FINGERS = 6
    TWO_FINGERS = 7
    ONE_FINGER = 8
    MOVE_TO_ME = 9
    MOVE_FROM_ME = 10



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
        if(self.landmarks):
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
    

    #Check if top or down is presented towards the camera
    def isPalmPresented(self):
        if(self.fingers[0].getLandMark(0)[3] > 0):
            return False
        else:
            return True

    
    #detect which gesture is active
    def detectGesture(self):
        for i, gesture in enumerate(self.gestureList):
            if(gesture.isActive()):
                return gesture
    

    #obtain move (switch between gestures)
    def obtainGestureMove(self, previousGesture):
        gesture = self.detectGesture()

        if(not self.isPalmPresented() and (previousGesture.getDescription() == GestureDescription.HAND_OPEN or previousGesture.getDescription() == GestureDescription.FOUR_FINGERS) and (gesture.getDescription() == GestureDescription.HAND_CLOSED or gesture.getDescription() == GestureDescription.ONE_FINGER)):
            return HandGesture(self.getHandDescription(), GestureDescription.MOVE_TO_ME, True)
        elif(self.isPalmPresented() and (previousGesture.getDescription() == GestureDescription.HAND_OPEN or previousGesture.getDescription() == GestureDescription.FOUR_FINGERS) and (gesture.getDescription() == GestureDescription.HAND_CLOSED or gesture.getDescription() == GestureDescription.ONE_FINGER)):
            return HandGesture(self.getHandDescription(), GestureDescription.MOVE_FROM_ME, True)
        elif(not self.isPalmPresented() and previousGesture.getDescription() == GestureDescription.MOVE_TO_ME and (gesture.getDescription() == GestureDescription.HAND_CLOSED or gesture.getDescription() == GestureDescription.ONE_FINGER)):
            return HandGesture(self.getHandDescription(), GestureDescription.MOVE_TO_ME, True) 
        elif(self.isPalmPresented() and previousGesture.getDescription() == GestureDescription.MOVE_FROM_ME and (gesture.getDescription() == GestureDescription.HAND_CLOSED or gesture.getDescription() == GestureDescription.ONE_FINGER)):
            return HandGesture(self.getHandDescription(), GestureDescription.MOVE_FROM_ME, True) 
        else:
            return gesture


    
    #Subsciption function for gestures on a single hand
    def setupGesture(self):
        self.gestureList = []

        if(len(self.fingers) >0 ):
            #Thumb up
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.THUMB_UP, True if (self.fingers[0].getLandMark(3)[2] < self.fingers[0].getLandMark(1)[2] and self.fingers[1].getLandMark(3)[2] < self.fingers[2].getLandMark(3)[2] and self.fingers[2].getLandMark(3)[2] < self.fingers[3].getLandMark(3)[2] and self.fingers[0].getLandMark(3)[2] < self.fingers[2].getLandMark(1)[2]) else False))
            #Thumb down
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.THUMB_DOWN, True if (self.fingers[0].getLandMark(3)[2] > self.fingers[0].getLandMark(1)[2] and self.fingers[1].getLandMark(3)[2] > self.fingers[2].getLandMark(3)[2] and self.fingers[2].getLandMark(3)[2] > self.fingers[3].getLandMark(3)[2] and self.fingers[0].getLandMark(3)[2] > self.fingers[2].getLandMark(1)[2]) else False))
            #All fingers up
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.HAND_OPEN, True if (self.fingers[0].isOpen() and self.fingers[1].isOpen() and self.fingers[2].isOpen() and self.fingers[3].isOpen() and self.fingers[4].isOpen()) else False))
            #Hand closed
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.HAND_CLOSED, True if (not self.fingers[0].isOpen() and not self.fingers[1].isOpen() and not self.fingers[2].isOpen() and not self.fingers[3].isOpen() and not self.fingers[4].isOpen()) else False))
            #OK sign
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.OK_SIGN, True if (abs(self.fingers[0].getLandMark(3)[1] - self.fingers[1].getLandMark(3)[1]) < OK_FINGER_DISTANCE and abs(self.fingers[0].getLandMark(3)[2] - self.fingers[1].getLandMark(3)[2]) < OK_FINGER_DISTANCE and self.fingers[2].isOpen() and self.fingers[3].isOpen() and self.fingers[4].isOpen()) else False))
            

            #Count amount fingers 
            numberFinger = 0
            for j, finger in enumerate(self.fingers):
                if(finger.isOpen()):
                    numberFinger = numberFinger + 1
            # 4 finger
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.FOUR_FINGERS, True if (numberFinger == 4) else False))
            # 3 fingers
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.THREE_FINGERS, True if (numberFinger == 3) else False))
            # 2 fingers
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.TWO_FINGERS, True if (numberFinger == 2) else False))
            # 1 finger
            self.gestureList.append(HandGesture(self.getHandDescription(), GestureDescription.ONE_FINGER, True if (numberFinger == 1) else False))  

        return self