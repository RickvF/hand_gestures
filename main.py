import cv2
from HandtrackingModule import handDetector


def main():
    detector = handDetector()

    while True:
        gestureList = []

        #Obtain all hand and finger information. Obtain all positions and draw points and line on the image
        img, hands = detector.obtainHands()   

        #Register all gestures to listen too
        detector = detector.setupGestures(hands)   

        
        for i, gesture in enumerate(detector.gestureList):
            if(gesture.isActive()):
                print(gesture.getDescription())
                break

        # numberFinger = 0

        # for i, hands in enumerate(hands):
        #     for j, finger in enumerate(hands.fingers):
        #         if(finger.isOpen()):
        #             numberFinger = numberFinger + 1

        # print(numberFinger)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()