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
        return id(self) == id(_other)
    
    def Append(self, _other, _breakpoint, _edges):
        self.next = _other
        _other.prev = self
        if self.rightHalfEdge is None:
            self.rightHalfEdge = HalfEdge(_breakpoint, _edges)
            _other.leftHalfEdge = self.rightHalfEdge
        else:
            _other.leftHalfEdge = HalfEdge(_breakpoint, _edges)

    def Size(self):
        currArc = self
        count = 1

        while currArc is not None:
            count += 1
            currArc = currArc.next
        
        return count

    @staticmethod
    def Remove(_prev, _toRemove, _next, _eventPosition, _edges):
        newHalfEdge = HalfEdge(_eventPosition, _edges) 
        if _prev is not None:
            _prev.next = _next
            _prev.rightHalfEdge.next = newHalfEdge
            _prev.rightHalfEdge = newHalfEdge
        if _next is not None:
            _next.prev = _prev
            _next.leftHalfEdge.next = newHalfEdge
            _next.leftHalfEdge = newHalfEdge

    @staticmethod
    def GetLast(_root):
        currArc = _root
        while currArc.next is not None:
            currArc = currArc.next
        return currArc

    @staticmethod
    def AsArray(_root):
        array = []
        currArc = _root
        while currArc is not None:
            array.append(currArc)
            currArc = currArc.next
        
        return array
    
    @staticmethod
    def Backtrack(_root):
        currArc = _root
        while currArc.prev is not None:
            currArc = currArc.prev
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
        self.circles = []
        self.snapshots = []

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
                
                Arc.Remove(associatedArc.prev, associatedArc, associatedArc.next, event.midPoint, self.halfEdges)

                self.CheckForCircleEvents(associatedArc.prev, self.sweepLine)
                self.CheckForCircleEvents(associatedArc.next, self.sweepLine)

                self.vertices.append(event.midPoint)
            
            self.queue.sort(key=lambda e: e.position.y)

            self.snapshots.append(Snapshot(Arc.AsArray(self.rootArc), self.sweepLine + 0.01))

        self.CompleteAllHalfEdges()
        self.CullEdges()
        return DCEL(self.vertices, self.halfEdges, None), self.circles, self.snapshots

    def InitSites(self, _points):
        for p in _points:
            self.queue.append(SiteEvent(p))

    def InsertNewSite(self, _newSite):
        currArc = self.rootArc
        while currArc is not None:
            intersectionPoint = self.GetLowestIntersectionPoint(_newSite, self.sweepLine)
            
            if intersectionPoint is not None:
                currArc.Append(Arc(_newSite, currArc, currArc.next), intersectionPoint, self.halfEdges)

                currArc = currArc.next # Advance the linked list

                if currArc.next is not None:
                    duplicate = Arc(currArc.prev.focus, currArc, currArc.next)
                    currArc.Append(duplicate, intersectionPoint, self.halfEdges)

                self.CheckForCircleEvents(currArc, self.sweepLine)
                self.CheckForCircleEvents(currArc.prev, self.sweepLine)
                self.CheckForCircleEvents(currArc.next, self.sweepLine)

                self.vertices.append(intersectionPoint)

                return
            
            currArc = currArc.next
        
        lastArc = Arc.GetLast(self.rootArc)
        newArc = Arc(_newSite, lastArc, None)
        lastArc.Append(newArc, Parabola.GetBreakpoint(lastArc, newArc, self.sweepLine, True), self.halfEdges)

    def GetLowestIntersectionPoint(self, _point, _sweepLine):
        intersectionPoint = None
        currArc = self.rootArc

        while currArc is not None:
            newIntersection = self.GetIntersectionPoint(_point, currArc, self.sweepLine)

            if newIntersection is not None:
                if intersectionPoint is None:
                    intersectionPoint = newIntersection
                elif newIntersection.y > intersectionPoint.y:
                    intersectionPoint = newIntersection

            currArc = currArc.next
        
        return intersectionPoint

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

    def CheckForCircleEvents(self, _arc, _sweepLine):
        if _arc is None: return False
        if _arc.prev is None or _arc.next is None: return False

        lowestPoint, midPoint = self.LowestPointOnCircumcircle(_arc.prev.focus, _arc.focus, _arc.next.focus)

        if lowestPoint is None: return False
        if lowestPoint.y > _sweepLine:
            self.queue.append(CircleEvent(lowestPoint, midPoint, _arc))
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

        if G == 0: return None, None

        midpoint = Vector((D * E - B * F) / G, (A * F - C * E) / G)
        radius = math.sqrt((a.x - midpoint.x) ** 2 + (a.y - midpoint.y) ** 2)
        lowestPoint = Vector(midpoint.x, midpoint.y + radius)

        self.circles.append(Circumcircle(_vectorA, _vectorB, _vectorC, midpoint, radius, lowestPoint))

        return Vector(midpoint.x, midpoint.y + radius), midpoint
            
    def CompleteAllHalfEdges(self):
        self.sweepLine = Settings.SCREEN_HEIGHT * 3
        
        currArc = self.rootArc
        while currArc is not None:
            if currArc.leftHalfEdge is not None:
                if currArc.leftHalfEdge.next is None:
                    leftEndVertex = Parabola.GetBreakpoint(currArc.prev, currArc, self.sweepLine, True)
                    if leftEndVertex is not None:
                        leftHalfEdgeNext = HalfEdge(leftEndVertex, self.halfEdges)
                        currArc.leftHalfEdge.next = leftHalfEdgeNext

            if currArc.rightHalfEdge is not None:
                if currArc.rightHalfEdge.next is None:
                    rightEndVertex = Parabola.GetBreakpoint(currArc, currArc.next, self.sweepLine, False)
                    if rightEndVertex is not None:
                        rightHalfEdgeNext = HalfEdge(rightEndVertex, self.halfEdges)
                        currArc.rightHalfEdge.next = rightHalfEdgeNext

            currArc = currArc.next
    
    def CullEdges(self):
        previousCount = len(self.halfEdges)
        index = 0

        while True:
            if index == len(self.halfEdges):
                break
            
            currHalfEdge = self.halfEdges[index]
            noDuplicates = True
            
            for i in range(len(self.halfEdges)):
                if i == index:
                    continue

                if currHalfEdge == self.halfEdges[i]:
                    self.halfEdges.pop(i)
                    noDuplicates = False
                    break
            
            if noDuplicates == True:
                index += 1     

        print("Removed", str(previousCount - len(self.halfEdges)), "halfedges.")
            
class Circumcircle:
    """DEBUG PURPOSES ONLY"""
    def __init__(self, _a, _b, _c, _midpoint, _radius, _lowestPoint):
        self.a = _a
        self.b = _b
        self.c = _c
        self.midpoint = _midpoint
        self.radius = _radius
        self.lowestPoint = _lowestPoint

class Snapshot:
    """DEBUG PURPOSES ONLY"""
    def __init__(self, _parabolas, _directrix):
        self.parabolas = _parabolas
        self.directrix = _directrix