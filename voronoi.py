import math
import pygame
from vector import Vector
from beachLine import BeachLine
from VoronoiEvent import *
from circumcircle import Circumcircle

# Structure of beachline is defined in the following manner: Point, Parabola, Point, Parabola, Point, ... , Point, Parabola, Point
class VoronoiDiagram:
    def __init__(self, _vertices: [Vector], _edges: [(Vector, Vector)]):
        self.vertices: [Vector] = []
        self.edges: [(Vector, Vector)] = []

class VoronoiGenerator:
    def __init__(self):
        self.sweepLine: float = 0.0
        self.pointsToConsider: [Vector] = []
        self.queue: [VoronoiEvent] = []
        self.beachLine: BeachLine = BeachLine()
        self.circumcircles: [Circumcircle] = []
        self.consideredCircumcircles: [Circumcircle] = []
        self.vertices: [Vector] = []

    def GenerateVoronoi(self, _points: [Vector]):
        self.pointsToConsider = _points.copy()

        for p in self.pointsToConsider:
            self.queue.append(SiteEvent(p))
        
        while len(self.queue) > 0:
            event = self.queue.pop()
            self.sweepLine = event.position.y
            
            if event.type is EventType.SITEEVENT:
                newParabola = event.HandleEvent()

                for p in self.pointsToConsider:
                    if event.position == p:
                        self.pointsToConsider.remove(p)
                        break 

                if len(self.beachLine.beachLineContainer) > 0:
                    closestParabola, index = self.GetClosestParabola(self.beachLine, self.sweepLine, event.position)
                    newParabolaReceipt = self.beachLine.Insert(index, newParabola)
                    closestParabolaReceipt = self.beachLine.Insert(index, closestParabola)
                    
                    # Create Circumcircles
                    if index - 2 >= 0:
                        self.GenerateCircumcircle(
                            newParabolaReceipt,
                            self.beachLine.beachLineContainer[index - 2].element.focus,
                            self.beachLine.beachLineContainer[index - 1].element.focus,
                            self.beachLine.beachLineContainer[index].element.focus)
                    if index - 1 >= 0 and index + 1 < len(self.beachLine.beachLineContainer):
                        self.GenerateCircumcircle(
                            newParabolaReceipt,
                            self.beachLine.beachLineContainer[index - 1].element.focus,
                            self.beachLine.beachLineContainer[index].element.focus,
                            self.beachLine.beachLineContainer[index + 1].element.focus)
                    if index + 2 < len(self.beachLine.beachLineContainer):
                        self.GenerateCircumcircle(
                            newParabolaReceipt,
                            self.beachLine.beachLineContainer[index].element.focus,
                            self.beachLine.beachLineContainer[index + 1].element.focus,
                            self.beachLine.beachLineContainer[index + 2].element.focus)
                else:
                    self.beachLine.Insert(0, newParabola)

            elif event.type is EventType.VERTEXEVENT:
                circumcircle: Circumcircle = event.HandleEvent()
                self.beachLine.Remove(circumcircle.generatingParabolaReceipt)
                self.vertices.append(circumcircle.midpoint)

        return self.beachLine, self.sweepLine, self.circumcircles, self.consideredCircumcircles, self.vertices

    def GetClosestParabola(self, _beachLine: BeachLine, _sweepLine: float, _point: Vector):
        parabola: Parabola = _beachLine.beachLineContainer[0].element
        index: int = 0
        for i in range(0, len(_beachLine.beachLineContainer)):
            if _beachLine.beachLineContainer[i].element.GetYValue(_point.x, _sweepLine) > parabola.GetYValue(_point.x, _sweepLine):
                parabola = _beachLine.beachLineContainer[i].element
                index = i

        return parabola, index

    def GenerateCircumcircle(self, _generatingParabola: Parabola, _vectorA: Vector, _vectorB: Vector, _vectorC: Vector):
        if _vectorA == _vectorB or _vectorA == _vectorC or _vectorB == _vectorC:
            return
        else:
            newCircumcircle = Circumcircle(_generatingParabola, _vectorA, _vectorB, _vectorC)
            newCircumcircle.Generate()

            if newCircumcircle.lowestPoint.y > self.sweepLine and newCircumcircle.NoneInCircle(self.pointsToConsider):
                self.queue.append(CircleEvent(newCircumcircle))
                self.consideredCircumcircles.append(newCircumcircle)
            self.circumcircles.append(newCircumcircle)