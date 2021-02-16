
class Vector:
    def __init__(self, _x: float, _y: float):
        self.x = _x
        self.y = _y

    def ToTuple(self):
        return (self.x, self.y)

    def ToString(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

