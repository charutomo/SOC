# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 23:58:58 2021

@author: Charissa
"""
import math 
def findHAngle(dx, dy):
  """Determines the angle with respect to the x axis of a segment
  of coordinates dx and dy
  """
  l = math.sqrt(dx*dx + dy*dy)
  if dy > 0:
    return math.acos(dx/l)
  else:
    return 2*math.pi - math.acos(dx/l)

class Vertex:
    def __init__(self,xcoordinate,ycoordinate):
        self.x = xcoordinate
        self.y = ycoordinate
        self.halfedge = []
    def equivalence(self,_others):
        if type(_others)== Vertex:
            if self.x ==  _others.x and self.y == _others.y:
                return True
            else:
                return False
        else:
            return False

    def sortededges(self):
        self.halfedge.sort(key=lambda a: a.angle, reverse=True)

class Edges:
    def __init__(self,point1,point2):
        self.prev = None
        self.next = None
        self.twin = None
        self.tail = point1
        self.face = None
        self.angle = findHAngle(point2.x-point1.x,point2.y-point1.y)
    def equivalence(self,_others):
        if self.tail == _others.tail and self.next.tail == _others.next.tail:
            return True
        else:
            return False
    def printedge(self):
        if self.next !=None:
            return (self.tail.x, self.tail.y,self.next.tail.x,self.next.tail.y)
        else:
            return self.tail.x, self.tail.y

class Face:
     def __init__(self):
         self.halfEdge = None
         self.variable = None
   
            
        
class DCEL:
    def __init__(self):
        self.vertex = []
        self.edge = []
        self.face = []
    
    def findVertex(self, x, y):
        for vert in self.vertex:
            if vert.x == x and vert.y == y:
                return vert
        else:
            return None
    def findhalfedge(self, v1, v2):
        for h in self.hedges:
            nextEdge = h.next
            if (h.tail.x == v1[0] and h.tail.y == v1[1]) and (nextEdge.tail.x == v2[0] and nextEdge.tail.y == v2[1]):
                return h
        else:
            return None
    
    def printDCEL(self,position,subdivide):
        for point in position:
            self.vertex.insert(-1,Vertex(point[0],point[1]))
        for section in subdivide:
            start = section[0]
            end = section[1]
            v1 = self.findVertex(start[0], start[1])
            v2 = self.findVertex(end[0], end[1])
            e1 = Edges(v1,v2)
            e2 = Edges (v2,v1)
            e1.twin = e2
            e2.twin = e1
            v1.halfedge.append(e1)
            v2.halfedge.append(e2)
            self.edge.append(e1)
            self.edge.append(e2)
            
        for v in self.vertex:
            v.sortededges()
            halfedgecount = len(v.halfedge)
            if halfedgecount <2:
                return ("DCEL cannot be produced as it is invalid, it requires at least 2 half edge. Please try again.")
            for i in range(0,halfedgecount-1):
                h1 = v.halfedge[i]
                h2 = v.halfedge[i+1]
                h1.twin.next = h2
                h2.prev = h1.twin
            h1 = v.halfedge[halfedgecount-1]
            h2 = v.halfedge[0]
            indexface = 0
            for he in self.edge:
                if he.face ==None:
                    indexface+=1
                face = Face()
                face.variable = str(indexface)
                face.he = he
                he.face = face
                h = he
                while h.next != he :
                    h.face = face
                    h = h.next
                h.face = face
                self.face.append(face)
    def findRegionGivenSegment(self, section):
        v1 = section[0]
        v2 = section[1]
        start = self.findHalfEdge(v1, v2)
        h = start
        while (not h.next == start):
          print(h)
          h = h.next
        print(h, start)
 
position = [(0, 5), (2, 5), (3, 0), (0, 0)]
subdivide = [
      [(0, 5), (2, 5)],
      [(2, 5), (3, 0)],
      [(3, 0), (0, 0)],
      [(0, 0), (0, 5)],
      [(0, 5), (3, 0)],
  ]

dcel1 = DCEL()
dcel1.printDCEL(position,subdivide)     
#dcel1.findRegionGivenSegment([(3, 0), (0, 5)])      

class Room_Allocation(DCEL):
    def __init__(self,pathway_width):
        self.width = pathway_width
    def rooms(self,position,subdivide):
        dcel = DCEL()
        dcel.printDCEL(position,subdivide)     
        return dcel
        