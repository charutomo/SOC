from collections import namedtuple
from VoronoiEvent import *
import math
import pygame

# Structure of beachline is defined in the following manner: Point, Parabola, Point, Parabola, Point, ... , Point, Parabola, Point
class BeachLine:
    def __init__(self):
        self.list = []

    def insert(self, _index, _newElement):
        self.list.insert(_index, _newElement)

    def append(self, _newElement):
        self.list.append(_newElement)

class VoronoiDiagram:
    def __init__(self, _vertices, _edges):
        self.vertices = []
        self.edges = []

class VoronoiGenerator:
    def GenerateVoronoi(self, _points):
        sweepLine = None
        beachLine = BeachLine()
        parabolas = []
        vertices = []
        edges = []
        queue = []
        for p in _points:
            queue.append(SiteEvent(p))

        while len(queue) > 0:
            event = queue.pop()
            
            if event.type is EventType.SITEEVENT:
                event.HandleEvent(sweepLine)
            elif event.type is EventType.VERTEXEVENT:
                event.HandleEvent()

        return VoronoiDiagram(vertices, edges)

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

    def Draw(self, _diagram, _surface : pygame.Surface):
        for e in _diagram.edges:
            pygame.draw.line(
                surface = _surface,
                color = pygame.Color(100, 100, 100),
                start_pos = e[0],
                end_pos = e[1],
                width = 1
            )
