import math
import pygame
import Settings
from vector import Vector
from VoronoiSite import VoronoiSite
from VoronoiEvent import *
from circumcircle import Circumcircle
from parabola import Parabola

# Structure of beachline is defined in the following manner: Point, Parabola, Point, Parabola, Point, ... , Point, Parabola, Point
class VoronoiDiagram:
    def __init__(self, _vertices: [Vector], _edges: [(Vector, Vector)]):
        self.vertices: [Vector] = []
        self.edges: [(Vector, Vector)] = []

class VoronoiGenerator:
    def __init__(self):
        self.sweepLine: float = 0.0
        self.queue: [VoronoiEvent] = []
        self.sites: [VoronoiSite] = []      # Parabolas are not actually saved. Only the factors used to create one
        self.sitesToConsider: [VoronoiSite] = []
        self.beachLine: [VoronoiSite] = []              # This is a list of sites not parabolas
        self.circumcircles: [Circumcircle] = []
        self.consideredCircumcircles: [Circumcircle] = []
        self.vertices: [Vector] = []

    def GenerateVoronoi(self, _points: [Vector]):
        for p in _points:
            newSite = VoronoiSite(p)
            self.sites.append(newSite)
            self.sitesToConsider.append(newSite)
            self.queue.append(SiteEvent(newSite))

        while len(self.queue) > 0:
            event = self.queue.pop(0)
            self.sweepLine = event.position.y
            
            if event.type is EventType.SITEEVENT:
                newSite = event.HandleEvent()

                if len(self.beachLine) > 0:
                    associatedSite, index = self.GetClosestParabola(self.beachLine, self.sweepLine, newSite)
                    self.beachLine.insert(index, newSite)
                    self.beachLine.insert(index, associatedSite)

                    # Create Circumcircles
                    if index - 2 >= 0:
                        self.GenerateCircumcircle(
                            self.beachLine[index + 1],
                            self.beachLine[index],
                            self.beachLine[index + 1],
                            self.beachLine[index + 2])
                    if index - 1 >= 0 and index + 1 < len(self.beachLine) - 1:
                        self.GenerateCircumcircle(
                            self.beachLine[index],
                            self.beachLine[index - 1],
                            self.beachLine[index],
                            self.beachLine[index + 1])
                    if index + 2 < len(self.beachLine) - 2:
                        self.GenerateCircumcircle(
                            self.beachLine[index + 1],
                            self.beachLine[index],
                            self.beachLine[index + 1],
                            self.beachLine[index + 2])
                else:
                    self.beachLine.insert(0, newSite)
            
            elif event.type is EventType.VERTEXEVENT:
                circumcircle: Circumcircle = event.HandleEvent()
                self.beachLine.remove(circumcircle.associatedSite)
                self.sitesToConsider.remove(circumcircle.associatedSite)
                self.vertices.append(circumcircle.midpoint)

            self.queue.sort(key=lambda e: e.position.y)

        return self.beachLine, self.sweepLine, self.circumcircles, self.consideredCircumcircles, self.vertices

    def GetClosestParabola(self, _beachLine: [VoronoiSite], _sweepLine: float, _site: [VoronoiSite]):
        parabola: Parabola = Parabola(_beachLine[0])
        dist =  parabola.position.y - Parabola.GetYValue(parabola, parabola.focus.x,_sweepLine) 
        for index in range(len(_beachLine)):
            if _beachLine[index].position.x ==_site.position.x:
               if _beachLine[index].position.y - Parabola.GetYValue(parabola, _beachLine[index].position.x,_sweepLine)<dist:
                   dist =  _beachLine[index].position.y - Parabola.GetYValue(parabola, _beachLine[index].position.x,_sweepLine)
        return _beachLine[index], index      
               
        #parabola: Parabola = _beachLine[0]
        #index: int = 0
        #while index < len(_beachLine):
            #if _beachLine[index].position.y > Parabola.GetYValue(parabola, _beachLine[index].position.x,_sweepLine):
                #parabola = _beachLine[index]
            #else:
                #break
            #index+=1
       

    def GenerateCircumcircle(self, _associatedSite: VoronoiSite, _siteA: VoronoiSite, _siteB: VoronoiSite, _siteC: VoronoiSite):
        if _siteA == _siteB or _siteA == _siteC or _siteB == _siteC:
            return
        else:
            newCircumcircle = Circumcircle(_associatedSite, _siteA, _siteB, _siteC)
            newCircumcircle.Generate()

            if newCircumcircle.lowestPoint.y > self.sweepLine and newCircumcircle.NoneInCircle(self.sitesToConsider):
                self.queue.append(CircleEvent(newCircumcircle))
                self.consideredCircumcircles.append(newCircumcircle)
            self.circumcircles.append(newCircumcircle)