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
        self.sitesToConsider: [VoronoiSite] = []
        self.beachLine: [VoronoiSite] = []              # This is a list of sites not parabolas
        self.vertices: [Vector] = []

    def GenerateVoronoi(self, _points: [Vector]):
        for p in _points:
            newSite = VoronoiSite(p)
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
                    if index != 0 or index != (len(self.beachLine) - 1):
                        self.beachLine.insert(index, associatedSite)

                    for i in range(0, len(self.beachLine) - 2):
                        self.GenerateCircumcircle(
                            self.beachLine[i + 1],
                            self.beachLine[i],
                            self.beachLine[i + 1],
                            self.beachLine[i + 2])
                else:
                    self.beachLine.insert(0, newSite)
            
            elif event.type is EventType.VERTEXEVENT:
                circumcircle: Circumcircle = event.HandleEvent()
                self.beachLine.remove(circumcircle.associatedSite)
                self.sitesToConsider.remove(circumcircle.associatedSite)
                self.vertices.append(circumcircle.midpoint)

            self.queue.sort(key=lambda e: e.position.y)

        print(len(self.vertices))
        return self.vertices

    def GetClosestParabola(self, _beachLine: [VoronoiSite], _sweepLine: float, _site: [VoronoiSite]):
        '''
        Parameters
        ----------
        _beachLine : [VoronoiSite]
            the sequences of beachlines
        _sweepLine : float
            sweepline
        _site : [VoronoiSite]
            event sites

        Returns
        -------
        _beachLine[index]: parabola
            the parabola most adjacent to the site 
        index : float
            the index of beachline that has the closest proximity to site

        '''
        index = 0
        parabola = Parabola(_beachLine[index].position)
        dist =  _site.position.EuclideanDistance(Vector(_site.position.x, parabola.GetYValue(_site.position.x,_sweepLine)))# finding the vertical distance between the parabola and site 
        for i in range(1,len(_beachLine)):
            if _beachLine[i].position.x ==_site.position.x:
               if _site.position.EuclideanDistance(Vector(_site.position.x, Parabola(_beachLine[i].position).GetYValue(_site.position.x,_sweepLine))) < dist: #finding the minimum distance between parabola and site 
                   dist =  _site.position.EuclideanDistance(Vector(_site.position.x, Parabola(_beachLine[i].position).GetYValue(_site.position.x,_sweepLine)))
                   index = i
        return _beachLine[index], index      
              
    def GenerateCircumcircle(self, _associatedSite: VoronoiSite, _siteA: VoronoiSite, _siteB: VoronoiSite, _siteC: VoronoiSite):
        if _siteA == _siteB or _siteA == _siteC or _siteB == _siteC:
            return
        else:
            newCircumcircle = Circumcircle(_associatedSite, _siteA, _siteB, _siteC)
            newCircumcircle.Generate()

            if newCircumcircle.lowestPoint.y > self.sweepLine and newCircumcircle.NoneInCircle(self.sitesToConsider):
                self.queue.append(CircleEvent(newCircumcircle))