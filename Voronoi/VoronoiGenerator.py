import pygame
from Geometry.Vector import Vector
from Geometry.Parabola import Parabola
from Voronoi.VoronoiEvent import (VoronoiEvent, SiteEvent, CircleEvent, EventType)
from DCEL.DCEL import (Vertex, HalfEdge, Face, DCEL)
import Settings
import math

class Arc(Parabola):
    def __init__(self, _site, _prev, _next):
        super().__init__(_site)
        self.prev = _prev
        self.next = _next
        self.leftHalfEdge = None
        self.rightHalfEdge = None

    def __eq__(self, _other):
        return self is _other

    def CreateBothHalfEdges(self, _breakpoint, _edges):
        self.CreateLeftHalfEdge(_breakpoint, _edges)
        self.CreateRightHalfEdge(_breakpoint, _edges)

    def CreateRightHalfEdge(self, _breakpoint, _edges):
        self.rightHalfEdge = HalfEdge(_breakpoint)
        _edges.append(self.rightHalfEdge)
    
    def CreateLeftHalfEdge(self, _breakpoint, _edges):
        self.leftHalfEdge = HalfEdge(_breakpoint)
        _edges.append(self.leftHalfEdge)
    
    def Append(self, _other, _breakpoint, _edges):
        self.next = _other

        if self.rightHalfEdge is None:
            self.CreateRightHalfEdge(_breakpoint, _edges)

        if _other.next is not None: 
            _other.next.prev = _other

            if _other.next.leftHalfEdge is None:
                _other.next.CreateLeftHalfEdge(_breakpoint, _edges)
        
        _other.CreateBothHalfEdges(_breakpoint, _edges)

    @staticmethod
    def Remove(_prev, _toRemove, _next, _eventPosition):
        newHalfEdge = HalfEdge(_eventPosition) 
        if _prev is not None:
            _prev.next = _next
            _prev.rightHalfEdge.AddNext(newHalfEdge)
        if _next is not None:
            _next.prev = _prev
            _next.leftHalfEdge.AddNext(newHalfEdge)

    @staticmethod
    def GetLast(_root):
        currArc = _root
        while currArc.next is not None:
            currArc = currArc.next
        return currArc

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
        self.vertices = []

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
                
                Arc.Remove(associatedArc.prev, associatedArc, associatedArc.next, event.position)

                self.CheckForCircleEvents(associatedArc.prev, event.position)
                self.CheckForCircleEvents(associatedArc.next, event.position)

                self.vertices.append(event.position)
            
            self.queue.sort(key=lambda e: e.position.y)

        self.CompleteAllHalfEdges()
        return DCEL(self.vertices, self.halfEdges, None)

    def InitSites(self, _points):
        for p in _points:
            self.queue.append(SiteEvent(p))

    def InsertNewSite(self, _newSite):
        currArc = self.rootArc
        while currArc is not None:
            intersectionPoint = self.GetIntersectionPoint(_newSite, currArc, self.sweepLine)
            
            if intersectionPoint is not None:
                newArc = Arc(_newSite, currArc, currArc.next)
                currArc.Append(newArc, intersectionPoint, self.halfEdges)

                currArc = currArc.next # Advance the linked list

                duplicate = Arc(currArc.prev.focus, currArc, currArc.next)
                currArc.Append(duplicate, intersectionPoint, self.halfEdges)
                
                self.CheckForCircleEvents(currArc, _newSite)
                self.CheckForCircleEvents(currArc.prev, _newSite)
                self.CheckForCircleEvents(currArc.next, _newSite)

                self.vertices.append(intersectionPoint)

                return
            
            currArc = currArc.next
        
        lastArc = Arc.GetLast(self.rootArc)
        newArc = Arc(_newSite, lastArc, None)
        lastArc.Append(newArc, Parabola.GetBreakpoint(lastArc, newArc, self.sweepLine, True), self.halfEdges)

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
        if _arc is None: return None
        if _point == _arc.focus: return None

        leftIntersection = Vector(0.0, 0.0)
        rightIntersection = Vector(0.0, 0.0)

        if _arc.prev is not None:
            leftIntersection = Parabola.GetBreakpoint(_arc.prev, _arc, _point.y, True)
        if _arc.next is not None:
            rightIntersection = Parabola.GetBreakpoint(_arc, _arc.next, _point.y, False)
        if (_arc.prev is None or _point.x >= leftIntersection.x) and (_arc.next is None or _point.x <= rightIntersection.x):
            return Vector(_point.x, _arc.GetValue(_point.x, _sweepLine))   

        return None 

    def CheckForCircleEvents(self, _arc, _newSite):
        if _arc is None: return False
        if _arc.prev is None or _arc.next is None: return False

        lowestPoint = self.LowestPointOnCircumcircle(_arc.prev.focus, _arc.focus, _arc.next.focus)

        if lowestPoint is None: return False
        if lowestPoint.y > _newSite.y: 
            print("Added New Circle Event")
            self.queue.append(CircleEvent(lowestPoint, _arc))
            return True

        return False

    def LowestPointOnCircumcircle(self, _vectorA, _vectorB, _vectorC):
        a = _vectorA
        b = _vectorB
        c = _vectorC

        #if (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0: return None

        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A * (a.x + b.x) + B * (a.y + b.y)
        F = C * (a.x + c.x) + D * (a.y + c.y)
        G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

        if G == 0: return None

        midpoint = Vector((D * E - B * F) / G, (A * F - C * E) / G)
        radius = math.sqrt((a.x - midpoint.x) ** 2 + (a.y - midpoint.y) ** 2)
        return Vector(midpoint.x, midpoint.y + radius)
            
    def CompleteAllHalfEdges(self):
        self.sweepLine = Settings.SCREEN_HEIGHT * 5

        currArc = self.rootArc
        while currArc is not None:
            if currArc.leftHalfEdge is not None:
                if currArc.leftHalfEdge.next is None:
                    leftEndVertex = Parabola.GetBreakpoint(currArc.prev, currArc, self.sweepLine, True)
                    if leftEndVertex is not None:
                        leftHalfEdgeNext = HalfEdge(leftEndVertex)
                        currArc.leftHalfEdge.next = leftHalfEdgeNext

            if currArc.rightHalfEdge is not None:
                if currArc.rightHalfEdge.next is None:
                    rightEndVertex = Parabola.GetBreakpoint(currArc, currArc.next, self.sweepLine, False)
                    if rightEndVertex is not None:
                        rightHalfEdgeNext = HalfEdge(rightEndVertex)
                        currArc.rightHalfEdge.next = rightHalfEdgeNext

            currArc = currArc.next
    
    def CullEdges(self):
        index = 0

        while True:
            if index == len(self.halfEdges):
                break
            
            currHalfEdge = self.halfEdges[index]

            index++
         