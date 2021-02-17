import Settings
from vector import Vector
from parabola import Parabola

class VoronoiSite:
    def __init__(self, _position: Vector):
        self.id: int = Settings.GenerateUniqueID()
        self.position: Vector = _position

        self.associatedParabola = Parabola(self.position)

    def Print(self):
        print("ID: " + str(self.id) + "\nPosition: " + self.position.ToString())

