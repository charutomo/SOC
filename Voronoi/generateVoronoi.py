from collections import namedtuple
from enum import Enum
import math

# Structure of beachline is defined in the following manner: Point, Parabola, Point, Parabola, Point, ... , Point, Parabola, Point
class BeachLine:
    def __init__(self):
        self.list = []

    def insert(self, _index, _newElement):
        self.list.insert(_index, _newElement)

class QueueItem:
    def __init__(self, _position, _type):
        self.position = _position
        self.type = _type

class QueueItemType(Enum):
    POINTEVENT = 1
    VERTEXEVENT = 2

class Parabola:
    def __init__(self, _focus, _directrix, _min, _max):
        self.focus = _focus
        self.directrix = _directrix
        self.range = (_min, _max)

    # Get the x value of a parabola given the y value
    # Note that x has to be bounded withn the range
    def GetYValue(self, _x):
        pass

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
                closestParabola, index = self.GetClosestParabola(beachLine, event.position)
                # Split it into half and then create a new parabola in between
                newParabola = Parabola(event.position, sweepLine)
                beachLine.insert(newParabola)

                pass
            elif event is QueueItemType.VERTEXEVENT:
                # Get the parabola that has been deleted
                parabola = None
                vertices.append(parabola.focus)
                pass

        return None

    def GetClosestParabola(self, _beachLine, _point):
        parabola = _beachLine[0]
        index = 0
        for i in range(0, len(_beachLine)):
            if self.EuclideanDistance(_point, _beachLine[i]) < self.EuclideanDistance(_point, parabola):
                parabola = _beachLine[i]
                index = i

        return parabola, index

    def EuclideanDistance(self, _pointA, _pointB):
        return math.sqrt((_pointA.x - _pointB.x) ^ 2 + (_pointA.y - _pointB.y) ^ 2)