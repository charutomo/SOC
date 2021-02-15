from collections import namedtuple
from VoronoiEvent import *
import math
import pygame

# Structure of beachline is defined in the following manner: Point, Parabola, Point, Parabola, Point, ... , Point, Parabola, Point
class VoronoiDiagram:
    def __init__(self, _vertices, _edges):
        self.vertices = []
        self.edges = []

class VoronoiGenerator:
    def GenerateVoronoi(self, _points):
        sweepLine = 0.0
        queue = []
        beachLine = []

        for p in _points:
            queue.append(SiteEvent(p))
        
        while len(queue) > 0:
            event = queue.pop()
            sweepLine = event.position[1]
            
            if event.type is EventType.SITEEVENT:
                newParabola = event.HandleEvent(sweepLine)

                if len(beachLine) > 0:
                    closestParabola, index = self.GetClosestParabola(beachLine, event.position)
                    beachLine.insert(index, newParabola)
                    if index != 0 and index != len(beachLine) - 1:
                        beachLine.insert(index, closestParabola)
                    pass
                else:
                    beachLine.append(newParabola)
                
                # Create Circumcircle

            elif event.type is EventType.VERTEXEVENT:
                event.HandleEvent()

        
        return beachLine

    def GetClosestParabola(self, _beachLine, _point):
        parabola = _beachLine[0]
        index = 0
        for i in range(0, len(_beachLine)):
            if _beachLine[i].GetYValue(_point[0]) > parabola.GetYValue(_point[0]):
                parabola = _beachLine[i]
                index = i

        return parabola, index

    def EuclideanDistance(self, _pointA, _pointB):
        return math.sqrt((_pointA.x - _pointB.x) ^ 2 + (_pointA.y - _pointB.y) ^ 2)

    def Draw(self, _diagram, _surface : pygame.Surface):
        for e in _diagram.edges:
            pygame.draw.line(
                surface = _surface,
                color = pygame.Color(100, 100, 100),
                start_pos = e[0],
                end_pos = e[1],
                width = 1
            )
