import pygame
from Geometry.Vector import Vector
from Geometry.Parabola import Parabola
from Voronoi.VoronoiEvent import (VoronoiEvent, SiteEvent, CircleEvent, EventType)
from DCEL.DCEL import (Vertex, HalfEdge, Face)
import Settings
import math

class Arc(Parabola):
    def __init__(self, _site, _prev, _next):
        super().__init__(_site)
        self.prev = _prev
        self.next = _next
        self.leftHalfEdge = None
        self.rightHalfEdge = None

        if self.prev is not None:
            self.leftHalfEdge = HalfEdge(_site)
        if self.next is not None:
            self.rightHalfEdge = HalfEdge(_site)
    
    def __eq__(self, _other):
        return self is _other

class VoronoiGenerator:
    """The class used to generate the Voronoi diagram.
    
    Attributes
    ----------
    sweepLine: float
        The object used to advance the algorithm
    beachLine: [Arc]:
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
        self.rootArc = None
        self.queue = []
        self.halfEdges = []

        self.topLeft = Vector(0.0, 0.0)
        self.bottomRight = Vector(0.0, 0.0)

    def GenerateVoronoi(self, _points):
        self.InitSites(_points)
        
        while len(self.queue) > 0:
            event = self.queue.pop(0)
            self.sweepLine = event.position.y

            if event.type is EventType.SITEEVENT:
                newSite = event.position

                if self.rootArc is None:
                    self.rootArc = Arc(newSite, None, None)
                    continue

                self.InsertNewSite(newSite)
            elif event.type is EventType.VERTEXEVENT:
                associatedArc = event.arc
                
                if associatedArc.prev is not None:
                    associatedArc.prev.next = associatedArc.next
                    self.LinkHalfEdges(associatedArc.prev.rightHalfEdge, HalfEdge(event.position))
                
                if associatedArc.next is not None:
                    associatedArc.next.prev = associatedArc.prev
                    self.LinkHalfEdges(associatedArc.next.leftHalfEdge, HalfEdge(event.position))

                if associatedArc.edge is not None:
                    associatedArc.edge.destination = event.position
                
                if associatedArc.prev is not None:
                    newEvent = self.CheckForCircleEvents(associatedArc.prev, event.position)
                    if newEvent is not None: self.queue.append(newEvent)
                if associatedArc.next is not None:
                    newEvent = self.CheckForCircleEvents(associatedArc.next, event.position)
                    if newEvent is not None: self.queue.append(newEvent)
            
            self.queue.sort(key=lambda e: e.position.y)

        self.CompleteAllHalfEdges()
        return self.halfEdges

    def InitSites(self, _points):
        for p in _points:
            self.queue.append(SiteEvent(p))

            if p.x < self.topLeft.x: 
                self.topLeft.x = p.x 
            if p.y < self.topLeft.y:
                self.topLeft.y = p.y
            if p.x > self.bottomRight.x:
                self.bottomRight.x = p.x
            if p.y > self.bottomRight.y:
                self.bottomRight.y = p.y

    def InsertNewSite(self, _newSite):
        currArc = self.rootArc
        while currArc is not None:
            intersectionPoint = self.GetIntersectionPoint(_newSite, currArc, self.sweepLine)
            
            if intersectionPoint is not None:
                newArc = self.AddToBeachLine(_newSite, currArc)
                
                self.LinkHalfEdges(newArc.prev.rightHalfEdge, newArc.leftHalfEdge)
                self.LinkHalfEdges(newArc.rightHalfEdge, newArc.next.leftHalfEdge)

                newEvent = self.CheckForCircleEvents(currArc, _newSite)
                if newEvent is not None: self.queue.append(newEvent)
                newEvent = self.CheckForCircleEvents(currArc.prev, _newSite)
                if newEvent is not None: self.queue.append(newEvent)
                newEvent = self.CheckForCircleEvents(currArc.next, _newSite)
                if newEvent is not None: self.queue.append(newEvent)

                return
            
            currArc = currArc.next
        
        lastArc = self.rootArc
        while lastArc.next is not None:
            lastArc = lastArc.next
        lastArc.next = Arc(_newSite, lastArc, None)

        start = Vector(0.0, 0.0)
        start.y = self.topLeft.y
        start.x = (lastArc.next.focus.x + lastArc.focus.x) / 2
        self.LinkHalfEdges(lastArc.rightHalfEdge, lastArc.next.leftHalfEdge)

    def AddToBeachLine(self, _site, _currArc):
        currArcCopy = Arc(_currArc.focus, _currArc.prev, _currArc)
        if currArcCopy.prev is not None: currArcCopy.prev.next = currArcCopy
        if _currArc.prev is not None: _currArc.prev = currArcCopy

        newArc = Arc(_site, currArcCopy, _currArc)
        if _currArc.prev is not None: _currArc.prev = newArc
        if currArcCopy.next is not None: currArcCopy.next = newArc

        return newArc

    def LinkHalfEdges(self, _halfEdgeA, _halfEdgeB):
        if _halfEdgeA is not None: _halfEdgeA.next = _halfEdgeB
        if _halfEdgeB is not None: _halfEdgeB.prev = _halfEdgeA

    def GetIntersectionPoint(self, _point, _arc, _sweepLine):
        """ Checks if a parabola created with focus at _point intersects with _arc

        Parameters
        ----------
        _point : Vector
            The point to check
        _arc: Arc
            The arc on the beachline
        _sweepLine : float
            The sweepline
        """
        if _arc is None:
            return None

        leftIntersection = Vector(0.0, 0.0)
        rightIntersection = Vector(0.0, 0.0)

        if _arc.prev is not None:
            leftIntersection = Parabola.GetBreakpoint(_arc.prev, _arc, _point.y)
        if _arc.next is not None:
            rightIntersection = Parabola.GetBreakpoint(_arc, _arc.next, _point.y)
        if (_arc.prev is None or _point.x >= leftIntersection.x) and (_arc.next is None or _point.x <= rightIntersection.x):
            return Vector(_point.x, _arc.GetValue(_point.x, _sweepLine))   

        return None 

    def LowestPointOnCircumcircle(self, _vectorA, _vectorB, _vectorC):
        a = _vectorA
        b = _vectorB
        c = _vectorC

        if (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0:
            return None

        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A * (a.x + b.x) + B * (a.y + b.y)
        F = C * (a.x + c.x) + D * (a.y + c.y)
        G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

        if G == 0: 
            return None

        midpoint = Vector((D * E - B * F) / G, (A * F - C * E) / G)
        radius = math.sqrt((a.x - midpoint.x) ** 2 + (a.y - midpoint.y) ** 2)
        return Vector(midpoint.x, midpoint.y + radius)

    def CheckForCircleEvents(self, _arc, _newSite):
        if _arc is None:
            return
        if _arc.prev is None or _arc.next is None:
            return

        lowestPoint = self.LowestPointOnCircumcircle(_arc.prev.focus, _arc.focus, _arc.next.focus)

        if lowestPoint.y > _newSite.y:
            return CircleEvent(lowestPoint, _arc)
            
    def CompleteAllHalfEdges(self):
        self.sweepLine = self.bottomRight.y + (self.bottomRight.y - self.topLeft.y) + (self.bottomRight.x - self.topLeft.x)

        currArc = self.rootArc
        while currArc is not None:
            if currArc.leftHalfEdge is not None:
                if currArc.leftHalfEdge.next is None:
                    currArc.leftHalfEdge.destination = Parabola.GetBreakpoint(currArc.prev, currArc, self.sweepLine)
                if currArc.leftHalfEdge.twin is None:
                    currArc.leftHalfEdge.twin = currArc.leftHalfEdge.CreateTwin()
                
                self.halfEdges.append(currArc.leftHalfEdge)
            if currArc.rightHalfEdge is not None:
                if currArc.rightHalfEdge.next is None:
                    currArc.rightHalfEdge.destination = Parabola.GetBreakpoint(currArc, currArc.next, self.sweepLine)
                if currArc.rightHalfEdge.twin is None:
                    currArc.rightHalfEdge.twin = currArc.rightHalfEdge.CreateTwin()
                
                self.halfEdges.append(currArc.rightHalfEdge)
            
            currArc = currArc.next