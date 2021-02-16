import math

class Vector:
    def __init__(self, _x: float, _y: float):
        self.x = _x
        self.y = _y

    def __eq__(self, _other):
        return math.isclose(self.x, _other.x) and math.isclose(self.y, _other.y)

    def ToTuple(self):
        return (self.x, self.y)

    def ToString(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def EuclideanDistance(self, _point):
        return ((self.x - _point.x) ** 2 + (self.y - _point.y) ** 2) ** (1/2)