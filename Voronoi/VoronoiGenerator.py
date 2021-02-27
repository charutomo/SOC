import pygame
from Geometry.Vector import Vector
from Geometry.Parabola import Parabola
from Geometry.Circumcircle import Circumcircle
from Voronoi.BeachLine import BeachLine
from Voronoi.VoronoiEvent import (VoronoiEvent, SiteEvent, CircleEvent, EventType)

class VoronoiGenerator:
    """The class used to generate the Voronoi diagram.
    
    Attributes
    ----------
    sweepLine: float
        The object used to advance the algorithm
    beachLine: [VoronoiSite]:
        The list of sites making up the parabolas
    queue: [VoronoiEvent]
        The priority queue used to contain the events
    sitesToConsider: [Vector]
        The list of sites yet to be handled
    vertices: [Vector]
        The vertices to be returned
    """
    def __init__(self):
        self.sweepLine = 0.0
        self.beachLine = BeachLine()
        self.queue = []
        self.sitesToConsider = []
        self.vertices = []

    def GenerateVoronoi(self, _points: [Vector]):
        self.InitSites(_points)
        
        while len(self.queue) > 0:
            event = self.queue.pop(0)
            self.sweepLine = event.position.y
            
            if event.type is EventType.SITEEVENT:
                newSite = event.HandleEvent()

                if len(self.beachLine.contents) > 0:
                    associatedSite, index = self.GetClosestParabola(self.beachLine, self.sweepLine, newSite)
                    self.beachLine.Insert(index, newSite)
                    if index != 0 or index != (len(self.beachLine.contents) - 1):
                        self.beachLine.Insert(index, associatedSite)

                    for i in range(0, len(self.beachLine.contents) - 2):
                        self.GenerateCircumcircle(
                            self.beachLine.contents[i],
                            self.beachLine.contents[i + 1],
                            self.beachLine.contents[i + 2],
                            Parabola(self.beachLine.contents[i + 1]))
                else:
                    self.beachLine.Insert(0, newSite)
            
            elif event.type is EventType.VERTEXEVENT:
                circumcircle: Circumcircle = event.HandleEvent()
                self.beachLine.RemoveSite(circumcircle.associatedParabola.focus)
                self.sitesToConsider.remove(circumcircle.associatedParabola.focus)
                self.vertices.append(circumcircle.midpoint)

            self.queue.sort(key=lambda e: e.position.y)

        return self.vertices

    def InitSites(self, _points):
        for p in _points:
            self.sitesToConsider.append(p)
            self.queue.append(SiteEvent(p))

    def GetClosestParabola(self, _beachLine, _sweepLine, _site):
        '''
        Parameters
        ----------
        _beachLine : Beachline
            The beachline data structure
        _sweepLine : float
            The sweepline
        _site : VoronoiSite
            The event site

        Returns
        -------
        _beachLine.contents[index]: parabola
            the parabola most adjacent to the site 
        index : float
            the index of beachline that has the closest proximity to site
        '''
        index = 0
        parabola = Parabola(_beachLine.contents[index])
        dist =  Vector.EuclideanDistance(_site, Vector(_site.x, parabola.GetValue(_site.x,_sweepLine))) # finding the vertical distance between the parabola and site 

        for i in range(1, len(_beachLine.contents)):
            if _beachLine.contents[i].x == _site.x:
                newDist = Vector.EuclideanDistance(_site, Vector(_site.x, Parabola(_beachLine.contents[i]).GetValue(_site.x,_sweepLine)))
                if newDist < dist: # finding the minimum distance between parabola and site 
                    dist =  newDist
                    index = i
        
        return _beachLine.contents[index], index      

    def GenerateCircumcircle(self, _siteA, _siteB, _siteC, _parabola):
        if _siteA == _siteB or _siteA == _siteC or _siteB == _siteC:
            return
        else:
            newCircumcircle = Circumcircle(_siteA, _siteB, _siteC, _parabola)
            newCircumcircle.Generate()

            if newCircumcircle.lowestPoint.y > self.sweepLine and Circumcircle.NoneInCircle(newCircumcircle, self.sitesToConsider):
                self.queue.append(CircleEvent(newCircumcircle))