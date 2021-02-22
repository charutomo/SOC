from Geometry.Vector import Vector

class VoronoiSite:
    def __init__(self, _position: Vector):
        self.position: Vector = _position

    def Print(self):
        print("Position: " + self.position.ToString())

