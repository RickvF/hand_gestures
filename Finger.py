

class Finger():
    def __init__(self, startIndex, landmarks, isThumb=False):
        self.startIndex = startIndex
        self.amountFingerPoints = 4
        self.isThumb = isThumb
        self.landmarks = landmarks
    
    def isOpen(self):
        if(not self.isThumb):
            if(self.landmarks[self.startIndex + 3][2] < self.landmarks[self.startIndex + 1][2]):
                return True
            else:
                return False
        else: #finger is a thump. Check how thumb is positioned
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