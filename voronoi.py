import math
import pygame
from vector import Vector
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
        self.queue = []
        self.beachLine = []
        self.circumcircles = []
        self.vertices = []

    def GenerateVoronoi(self, _points: [Vector]):
        for p in _points:
            self.queue.append(SiteEvent(p))
        
        while len(self.queue) > 0:
            event = self.queue.pop()
            self.sweepLine = event.position.y
            
            if event.type is EventType.SITEEVENT:
                newParabola = event.HandleEvent()

                if len(self.beachLine) > 0:
                    closestParabola, index = self.GetClosestParabola(self.beachLine, self.sweepLine, event.position)
                    self.beachLine.insert(index, newParabola)
                    if index != 0 and index != len(self.beachLine) - 1:
                        self.beachLine.insert(index, closestParabola)
                    
                    # Create Circumcircles
                    if index - 2 >= 0:
                        self.GenerateCircumcircle(
                            self.beachLine[index - 2].focus,
                            self.beachLine[index - 1].focus,
                            self.beachLine[index].focus)
                    if index - 1 >= 0 and index + 1 < len(self.beachLine):
                        self.GenerateCircumcircle(
                            self.beachLine[index - 1].focus,
                            self.beachLine[index].focus,
                            self.beachLine[index + 1].focus)
                    if index + 2 < len(self.beachLine):
                        self.GenerateCircumcircle(
                            self.beachLine[index].focus,
                            self.beachLine[index + 1].focus,
                            self.beachLine[index + 2].focus)
                else:
                    self.beachLine.append(newParabola)

            elif event.type is EventType.VERTEXEVENT:
                newVertex = event.HandleEvent()
                self.vertices.append(newVertex)

        for c in self.circumcircles:
            c.Print()

        return self.beachLine, self.sweepLine, self.circumcircles, self.vertices

    def GetClosestParabola(self, _beachLine: [], _sweepLine: float, _point: Vector):
        parabola: Parabola = _beachLine[0]
        index: int = 0
        for i in range(0, len(_beachLine)):
            if _beachLine[i].GetYValue(_point.x, _sweepLine) > parabola.GetYValue(_point.x, _sweepLine):
                parabola = _beachLine[i]
                index = i

        return parabola, index

    def GenerateCircumcircle(self, _vectorA: Vector, _vectorB: Vector, _vectorC: Vector):
        if _vectorA == _vectorB or _vectorA == _vectorC or _vectorB == _vectorC:
            return
        else:
            newCircumcircle = Circumcircle(_vectorA, _vectorB, _vectorC)
            newCircumcircle.Generate()
            self.circumcircles.append(newCircumcircle)
            self.queue.append(CircleEvent(newCircumcircle))