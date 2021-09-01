import cv2
import mediapipe as mp
from mediapipe.python.solutions import hands
from Hand import Hand
from FingerGesture import FingerGesture
from HandGesture import HandGesture
from Gesture import Gesture


class handDetector():
    def __init__(self, videoSource=0, mode=False, maxHands=2, detectionCon=0.7, trackingCon=0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, 
                                        self.maxHands, 
                                        self.detectionCon, 
                                        self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.cap = cv2.VideoCapture(videoSource)

        self.gestureList = []
    
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        handsCount = 0

        if self.results.multi_hand_landmarks:
            handsCount = len(self.results.multi_hand_landmarks)
            for handLms in self.results.multi_hand_landmarks:   
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) 

        return img, handsCount
    
    #get all positions of a hand. Pass the hand number to specify which hand to obtain
    def findPosition(self, img, handNmb=0, draw=True): 
        landmarksList = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNmb]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarksList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) 
        
        isleftHand = True
        if(self.results.multi_handedness):
            handInfo = self.results.multi_handedness[handNmb]
            if(handInfo.classification[0].label == "Left"):
                isleftHand = False

        return Hand(landmarksList, isleftHand)  
    

    # Get all hands and fingers in the captured image. Draw dots and lines too
    def obtainHands(self):
        success, img = self.cap.read()

        img, handsCount = self.findHands(img)

        hands = []
        for i in range(0, handsCount):
            hands.append(self.findPosition(img, i))
        
        return img, hands   

    def setupGestures(self, hands):
        self.gestureList = []

        for i, hands in enumerate(hands):
            self.gestureList.append(HandGesture(hands.getHandDescription() +  " hand open", True if (hands.fingers[0].isOpen() and hands.fingers[1].isOpen() and hands.fingers[2].isOpen() and hands.fingers[3].isOpen() and hands.fingers[4].isOpen()) else False))
            for j, finger in enumerate(hands.fingers):
                # self.gestureList.append(FingerGesture("Finger " + str(j) + " open", True if finger.isOpen() else False))
                break
        
        return self
