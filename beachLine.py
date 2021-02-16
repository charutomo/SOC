from parabola import Parabola

class BeachLineElement:
    def __init__(self, _id: int, _element):
        self.id: int = _id
        self.element = _element

class BeachLine:
    def __init__(self):
        self.internalCounter: int = 0
        self.beachLineContainer: [BeachLineElement] = []
    
    def Insert(self, _index: int, _parabola: Parabola):
        newBeachLineElement = BeachLineElement(self.internalCounter, _parabola)
        self.beachLineContainer.insert(_index, newBeachLineElement)
        self.internalCounter += 1
        return newBeachLineElement.id
    
    def Remove(self, _receipt: int):
        for element in self.beachLineContainer:
            if element.id == _receipt:
                self.beachLineContainer.remove(element)
                break