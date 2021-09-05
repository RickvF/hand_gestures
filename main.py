import cv2
from HandtrackingModule import handDetector


def main():
    detector = handDetector()

    while True:

        #Obtain all hand and finger information. Obtain all positions and draw points and line on the image
        img, hands = detector.obtainHands(draw=True)   

        #Check which gestures are active per hand
        currentGestures = detector.obtainGesture()

        #Show all data on the image
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()