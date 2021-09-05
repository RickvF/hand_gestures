from Gesture import Gesture


class FingerGesture(Gesture):
    def __init__(self, hand, description, condition):
        super().__init__(hand, description, condition)