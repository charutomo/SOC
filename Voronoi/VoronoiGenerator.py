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
                    associatedArc.prev.rightHalfEdge.twin = HalfEdge(event.position)
                    associatedArc.prev.rightHalfEdge.twin.next = associatedArc.prev.rightHalfEdge.prev
                    associatedArc.prev.rightHalfEdge.twin.prev = associatedArc.prev.rightHalfEdge.next
                
                if associatedArc.next is not None:
                    associatedArc.next.prev = associatedArc.prev
                    associatedArc.next.leftHalfEdge.twin = HalfEdge(event.position)
                    associatedArc.next.leftHalfEdge.twin.next = associatedArc.prev.leftHalfEdge.prev
                    associatedArc.next.leftHalfEdge.twin.prev = associatedArc.prev.leftHalfEdge.next
                
                if associatedArc.prev is not None:
                    newEvent = self.CheckForCircleEvents(associatedArc.prev, event.position)
                    if newEvent is not None: self.queue.append(newEvent)
                if associatedArc.next is not None:
                    newEvent = self.CheckForCircleEvents(associatedArc.next, event.position)
                    if newEvent is not None: self.queue.append(newEvent)
            
            self.queue.sort(key=lambda e: e.position.y)

        self.CompleteAllHalfEdges()
        return self.halfEdges, self.rootArc

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

            print(p.ToString())

    def InsertNewSite(self, _newSite):
        currArc = self.rootArc
        while currArc is not None:
            intersectionPoint = self.GetIntersectionPoint(_newSite, currArc, self.sweepLine)
            
            if intersectionPoint is not None:
                self.AddToBeachLine(_newSite, currArc, intersectionPoint)
                currArc = currArc.next # Advance the linked list
                self.AddToBeachLine(currArc.prev.focus, currArc, intersectionPoint)
                
                newEvent = self.CheckForCircleEvents(currArc, _newSite)
                if newEvent is not None: 
                    self.queue.append(newEvent)
                newEvent = self.CheckForCircleEvents(currArc.prev, _newSite)
                if newEvent is not None: 
                    self.queue.append(newEvent)
                newEvent = self.CheckForCircleEvents(currArc.next, _newSite)
                if newEvent is not None: 
                    self.queue.append(newEvent)

                return
            
            currArc = currArc.next
        
        lastArc = self.rootArc
        while lastArc.next is not None:
            lastArc = lastArc.next
        lastArc.next = Arc(_newSite, lastArc, None)

        start = Vector(0.0, 0.0)
        start.y = self.topLeft.y
        start.x = (lastArc.next.focus.x + lastArc.focus.x) / 2

    def AddToBeachLine(self, _site, _currArc, _intersectionPoint):
        newArc = Arc(_site, _currArc, _currArc.next)
        if _currArc.next is not None:
            _currArc.next.prev = newArc
        _currArc.next = newArc

    def DisplayBeachLine(self):
        currArc = self.rootArc
        while currArc is not None:
            print("Focus:", currArc.focus.ToString())
            currArc = currArc.next

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

        if _point == _arc.focus:
            return None

        leftIntersection = Vector(0.0, 0.0)
        rightIntersection = Vector(0.0, 0.0)

        if _arc.prev is not None:
            leftIntersection = Parabola.GetBreakpoint(_arc.prev, _arc, _point.y, True)
        if _arc.next is not None:
            rightIntersection = Parabola.GetBreakpoint(_arc, _arc.next, _point.y, False)
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

        if lowestPoint is None:
            return

        if lowestPoint.y > _newSite.y:
            return CircleEvent(lowestPoint, _arc)
            
    def CompleteAllHalfEdges(self):
        self.sweepLine = self.bottomRight.y + (self.bottomRight.y - self.topLeft.y) + (self.bottomRight.x - self.topLeft.x)

        self.DisplayBeachLine()

        currArc = self.rootArc
        while currArc is not None:
            if currArc.leftHalfEdge is None:
                currArc.leftHalfEdge = HalfEdge(currArc.rightHalfEdge.origin)
                #currArc.leftHalfEdge.destination = Parabola.GetBreakpoint(currArc.prev, currArc, self.sweepLine)
                currArc.leftHalfEdge.twin = currArc.leftHalfEdge.CreateTwin()
                
                self.halfEdges.append(currArc.leftHalfEdge)
            if currArc.rightHalfEdge is None:
                currArc.rightHalfEdge = HalfEdge(currArc.leftHalfEdge.origin)
                #currArc.rightHalfEdge.destination = Parabola.GetBreakpoint(currArc, currArc.next, self.sweepLine)
                currArc.rightHalfEdge.twin = currArc.rightHalfEdge.CreateTwin()
                
                self.halfEdges.append(currArc.rightHalfEdge)
            
            currArc = currArc.next