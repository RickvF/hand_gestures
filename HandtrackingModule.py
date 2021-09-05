from HandGesture import HandGesture
import cv2
import mediapipe as mp
from mediapipe.python.solutions import hands
from Hand import GestureDescription, Hand

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

        #List of all Hand objects
        self.handsInformation = []
        #List of the current active gestures
        self.currentGestures = []

    #Find the amount of hands in the view
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
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int((lm.z - hand.landmark[0].z)*100)
                landmarksList.append([id, cx, cy, cz])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) 
        
        isleftHand = True
        if(self.results.multi_handedness):
            handInfo = self.results.multi_handedness[handNmb]
            if(handInfo.classification[0].label == "Left"):
                isleftHand = False

        return Hand(landmarksList, isleftHand)  
    

    # Get all hands and fingers in the captured image. Draw dots and lines too
    def obtainHands(self, draw=True):
        success, img = self.cap.read()

        img, handsCount = self.findHands(img, draw)

        self.handsInformation = []
        for i in range(0, handsCount):
            self.handsInformation.append(self.findPosition(img, i, draw))
        
        return img, self.handsInformation   
    
    
    #detect which gesture is active per hand
    def obtainGesture(self):
        for j, hand in enumerate(self.handsInformation):
            #Get the previous hand gesture in order to obtain a detection of move between gestures
            hand_index = next((index for (index, d) in enumerate(self.currentGestures) if d["hand"] == hand.getHandDescription()), -1)
            previous_gesture = HandGesture("", GestureDescription.NONE, False)
            
            if(hand_index > -1):
                previous_gesture = self.currentGestures[hand_index]["gesture"]

            #Obtain active gesture or move
            gesture = hand.obtainGestureMove(previous_gesture)

            #check if this hand is already saved in the result
            if(hand_index > -1):           
                #if previous is different than new gesture, change previous gesture
                if(not (self.currentGestures[hand_index]["gesture"].getDescription() == gesture.getDescription())):
                    #Trigger a gesture change
                    self.gestureTrigger(hand, gesture)

                #Save the current gesture in the gesture list
                self.currentGestures[hand_index]["gesture"] = gesture
            else:
                self.currentGestures.append({"hand": hand.getHandDescription(), "gesture": gesture})
        
        self.completeGestureListTwoHands()
        
        return self.currentGestures
    

    #funtion to trigger when gesture change
    def gestureTrigger(self, hand, gesture):
        print(hand.getHandDescription() + " " + str(gesture.getDescription()) + "\n")
    

    #Fill current gestures always up to two hands eventhough 2 hands are not present on the screen
    def completeGestureListTwoHands(self):
        if(len(self.handsInformation) < 2):
            if(len(self.handsInformation) == 0):
                self.completeGestureListHand("Left")
                self.completeGestureListHand("Right")
            else:
                self.completeGestureListHand(self.handsInformation[0].getHandDescription())
    
    #Fill current gesture always up to two hands eventhough 2 hands are not present on the screen
    def completeGestureListHand(self, presentHand):
        if(presentHand == "Left"):
            hand_index = next((index for (index, d) in enumerate(self.currentGestures) if d["hand"] == "Right"), -1)
            if(hand_index > -1):
                if(not(self.currentGestures[hand_index]["gesture"].getDescription() == GestureDescription.NONE)):
                    self.gestureTrigger(Hand(None, False), HandGesture("", GestureDescription.NONE, False))
                self.currentGestures[hand_index]["gesture"] = HandGesture("", GestureDescription.NONE, False)
            else:
                self.currentGestures.append({"hand": "Right", "gesture": HandGesture("", GestureDescription.NONE, False)})
                self.gestureTrigger(Hand(None, False), HandGesture("", GestureDescription.NONE, False))
        else:
            hand_index = next((index for (index, d) in enumerate(self.currentGestures) if d["hand"] == "Left"), -1)
            if(hand_index > -1):
                if(not(self.currentGestures[hand_index]["gesture"].getDescription() == GestureDescription.NONE)):
                    self.gestureTrigger(Hand(None, True), HandGesture("", GestureDescription.NONE, False))
                self.currentGestures[hand_index]["gesture"] = HandGesture("", GestureDescription.NONE, False)
            else:
                self.currentGestures.append({"hand": "Left", "gesture": HandGesture("", GestureDescription.NONE, False)})
                self.gestureTrigger(Hand(None, True), HandGesture("", GestureDescription.NONE, False)) 
        

