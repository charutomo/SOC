import pygame
from Geometry.Vector import Vector
from Geometry.Parabola import Parabola
from Geometry.Circumcircle import Circumcircle
from Voronoi.VoronoiEvent import (VoronoiEvent, SiteEvent, CircleEvent, EventType)
from DCEL.DCEL import (Vertex, HalfEdge, Edge, Face)
import Settings

class Arc(Parabola):
    def __init__(self, _site, _prev, _next):
        super().__init__(_site)
        self.prev = _prev
        self.next = _next
        self.leftHalfEdge = None
        self.rightHalfEdge = None
        self.event = None
    
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
        self.beachLine = []
        self.queue = []
        self.edges = []

        self.smallestYValue = Settings.SCREEN_HEIGHT

    def GenerateVoronoi(self, _points):
        self.InitSites(_points)
        
        while len(self.queue) > 0:
            event = self.queue.pop(0)
            self.sweepLine = event.position.y

            if event.type is EventType.SITEEVENT:
                newSite = event.HandleEvent()

                if len(self.beachLine) < 1:
                    self.beachLine.append(Arc(newSite, None, None))
                    continue

                self.InsertNewSite(newSite)
            elif event.type is EventType.VERTEXEVENT:
                newHalfEdge = HalfEdge(event.position)
                associatedArc = event.HandleEvent()
                
                if associatedArc.prev is not None:
                    associatedArc.prev.next = associatedArc.next
                    associatedArc.prev.rightHalfEdge = newHalfEdge
                
                if associatedArc.next is not None:
                    associatedArc.next.prev = associatedArc.prev
                    associatedArc.next.leftHalfEdge = newHalfEdge

                if associatedArc.leftHalfEdge is not None:
                    associatedArc.leftHalfEdge.Complete(event.position)
                if associatedArc.rightHalfEdge is not None:
                    associatedArc.rightHalfEdge.Complete(event.position)
                
                if associatedArc.prev is not None:
                    newEvent = self.CheckForCircleEvents(associatedArc.prev, event.position)
                    if newEvent is not None: self.queue.append(newEvent)
                if associatedArc.next is not None:
                    newEvent = self.CheckForCircleEvents(associatedArc.next, event.position)
                    if newEvent is not None: self.queue.append(newEvent)

            self.queue.sort(key=lambda e: e.position.y)

        self.CompleteAllHalfEdges()
        print(len(self.edges))
        return self.edges

    def InitSites(self, _points):
        for p in _points:
            self.queue.append(SiteEvent(p))
            if p.y < self.smallestYValue:
                self.smallestYValue = p.y

    def InsertNewSite(self, _newSite):
        for i in range(len(self.beachLine)):
            currArc = self.beachLine[i]
            intersectionPoint = self.GetIntersectionPoint(_newSite, currArc, self.sweepLine)
            
            if intersectionPoint is not None:
                if (currArc.next is not None and self.GetIntersectionPoint(_newSite, currArc.next, self.sweepLine) is None):
                    currArc.next.prev = Arc(currArc.focus, currArc, currArc.next)
                    currArc.next = currArc.next.prev
                else:
                    currArc.next = Arc(currArc.focus, currArc, None)
                currArc.next.rightHalfEdge = currArc.rightHalfEdge

                currArc.next.prev = Arc(_newSite, currArc, currArc.next)
                currArc.next = currArc.next.prev
                
                nextArc = currArc.next

                nextArc.prev.rightHalfEdge = HalfEdge(intersectionPoint)
                nextArc.leftHalfEdge = nextArc.prev.rightHalfEdge
                self.edges.append(nextArc.prev.rightHalfEdge)

                nextArc.next.leftHalfEdge = HalfEdge(intersectionPoint)
                nextArc.rightHalfEdge = nextArc.next.leftHalfEdge
                self.edges.append(nextArc.next.leftHalfEdge)

                newEvent = self.CheckForCircleEvents(nextArc, _newSite)
                if newEvent is not None: self.queue.append(newEvent)
                newEvent = self.CheckForCircleEvents(nextArc.prev, _newSite)
                if newEvent is not None: self.queue.append(newEvent)
                newEvent = self.CheckForCircleEvents(nextArc.next, _newSite)
                if newEvent is not None: self.queue.append(newEvent)

                return
            
        lastArc = self.beachLine[-1]
        lastArc.next = Arc(_newSite, lastArc, None)

        start = Vector(0.0, 0.0)
        start.y = self.smallestYValue
        start.x = (lastArc.next.focus.x + lastArc.focus.x) / 2
        lastArc.rightHalfEdge = HalfEdge(start)
        lastArc.next.leftHalfEdge = lastArc.rightHalfEdge

    def GetIntersectionPoint(self, _point, _arc, _sweepLine):
        """
        Parameters
        ----------
        _point : Vector
            The point to check
        _arc: Arc
            The arc on the beachline
        _sweepLine : float
            The sweepline
        """
        leftIntersection = Vector(0.0, 0.0)
        rightIntersection = Vector(0.0, 0.0)

        if _arc.prev is not None:
            leftIntersection = Parabola.GetBreakpoint(_arc.prev, _arc, _point.x)
        if _arc.next is not None:
            rightIntersection = Parabola.GetBreakpoint(_arc, _arc.next, _point.x)
        if (_arc.prev is not None or _point.x >= leftIntersection.x) and (_arc.next is not None or _point.x <= rightIntersection.x):
            return Vector(_arc.GetValue(_point.y, _sweepLine), _point.y)   

        return None 

    def CheckForCircleEvents(self, _arc, _newSite):
        if _arc.prev is not None or _arc is not None or _arc.next is not None:
            return
        if _arc.prev == _arc or _arc.prev == _arc.next or _arc == _arc.next:
            return
            
        newCircumcircle = Circumcircle(_arc.prev.focus, _arc.focus, _arc.next.focus)
        newCircumcircle.Generate()
        
        if newCircumcircle.lowestPoint.y > _newSite.y:
            return CircleEvent(newCircumcircle, _arc)

    def CompleteAllHalfEdges(self):
        self.sweepLine = Settings.SCREEN_HEIGHT * 2

        for i in range(len(self.beachLine)):
            currArc = self.beachLine[i]
            if currArc.rightHalfEdge is not None:
                currArc.rightHalfEdge.Complete(self.GetIntersectionPoint(currArc.focus, currArc.next, self.sweepLine))
