import math
import pygame
from vector import Vector
from VoronoiEvent import *


# Structure of beachline is defined in the following manner: Point, Parabola, Point, Parabola, Point, ... , Point, Parabola, Point
class VoronoiDiagram:
    def __init__(self, _vertices: [Vector], _edges: [(Vector, Vector)]):
        self.vertices: [Vector] = []
        self.edges: [(Vector, Vector)] = []

class VoronoiGenerator:
    def GenerateVoronoi(self, _points: [Vector]):
        sweepLine: float = 0.0
        queue = []
        beachLine = []

        for p in _points:
            queue.append(SiteEvent(p))
        
        while len(queue) > 0:
            event = queue.pop()
            sweepLine = event.position.y
            
            if event.type is EventType.SITEEVENT:
                newParabola = event.HandleEvent()

                if len(beachLine) > 0:
                    closestParabola, index = self.GetClosestParabola(beachLine, sweepLine, event.position)
                    beachLine.insert(index, newParabola)
                    if index != 0 and index != len(beachLine) - 1:
                        beachLine.insert(index, closestParabola)
                    pass
                else:
                    beachLine.append(newParabola)
                
                # Create Circumcircle

            elif event.type is EventType.VERTEXEVENT:
                event.HandleEvent()


        return beachLine, sweepLine

    def GetClosestParabola(self, _beachLine: [], _sweepLine: float, _point: Vector):
        parabola: Parabola = _beachLine[0]
        index: int = 0
        for i in range(0, len(_beachLine)):
            if _beachLine[i].GetYValue(_point.x, _sweepLine) > parabola.GetYValue(_point.x, _sweepLine):
                parabola = _beachLine[i]
                index = i

        return parabola, index
