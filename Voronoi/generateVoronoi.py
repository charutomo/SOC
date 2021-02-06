from collections import namedtuple
from enum import Enum
import math

# Structure of beachline is defined in the following manner: Point, Parabola, Point, Parabola, Point, ... , Point, Parabola, Point
class BeachLine:
    def __init__(self):
        pass

class QueueItem:
    def __init__(self, _position, _type):
        self.position = _position
        self.type = _type

class QueueItemType(Enum):
    POINTEVENT = 1
    VERTEXEVENT = 2

class Parabola:
    def __init__(self, _focus, _directrix):
        self.focus = _focus
        self.directrix = _directrix

    def Split(self):
        return []

class VoronoiGenerator:
    Voronoi = namedtuple("Points", "Edges")

    def GenerateVoronoi(self, _points):
        sweepLine = None
        beachLine = BeachLine()
        parabolas = []
        vertices = []
        queue = []
        for p in _points:
            queue.append(QueueItem(p, QueueItemType.POINTEVENT))

        while len(queue) > 0:
            event = queue.pop()

            if event is QueueItemType.POINTEVENT:
                # Get closest parabola
                closestParabola = self.GetClosestParabola(beachLine, event.position)
                # Split it into half and then create a new parabola in between
                newParabola = Parabola(event.position, sweepLine)

                pass
            elif event is QueueItemType.VERTEXEVENT:
                pass

        return None

    def GetClosestParabola(self, _beachLine, _point):
        parabola = _beachLine[0]
        for p in _beachLine:
            if self.EuclideanDistance(_point, p) < self.EuclideanDistance(_point, parabola):
                parabola = p

        return parabola

    def EuclideanDistance(self, _pointA, _pointB):
        return math.sqrt((_pointA.x - _pointB.x) ^ 2 + (_pointA.y - _pointB.y) ^ 2)