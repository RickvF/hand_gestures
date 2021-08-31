import cv2
from HandtrackingModule import handDetector

def main():
    detector = handDetector()

    while True:
        img, hands = detector.obtainHands()        

        numberFinger = 0

        for i, hands in enumerate(hands):
            for j, finger in enumerate(hands.fingers):
                if(finger.isOpen()):
                    numberFinger = numberFinger + 1

        print(numberFinger)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()