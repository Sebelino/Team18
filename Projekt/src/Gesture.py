class Gesture:
    def __init__(self, name, multitouch, stringRepresentation):
        self.name = name
        self.multitouch = multitouch
        self.stringRepresentation = stringRepresentation

    def toString(self):
        return self.stringRepresentation
