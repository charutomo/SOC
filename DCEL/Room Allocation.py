# -*- coding: utf-8 -*-
"""
Created on Tue Mar 2 23:58:58 2021

@author: Charissa
"""
import math 

def findHAngle(x, y):
 
    '''
     Find the angle wrt the x axis with delta x and y coordinates

    Parameters
    ----------
    x : x coordinates
    y : y coordinates

    Returns
    -------
    angle
        return angle wrt the x axis with delta x and y coordinates

    '''
    l = math.sqrt(x**2 + y**2)
    if y > 0:
      return math.acos(x/l)
    else:
      return 2*math.pi - math.acos(x/l)

class Vertex:
    '''Vertex of DCEL'''
    def __init__(self, xcoordinate, ycoordinate):
        self.x = xcoordinate
        self.y = ycoordinate
        self.halfedge = []
    
    def equivalence(self,_others):
        '''
        To check if vertex is equivalent to other vertex

        Parameters
        ----------
        _others : Vertex
            

        Returns
        -------
        bool
            True if they are the same vertex and False if otherwise

        '''
        if type(_others)== Vertex:
            if self.x == _others.x and self.y == _others.y:
                return True
            else:
                return False
        else:
            return False

    def sortededges(self):
        '''
        sort half edges according to the angles wrt to x axis

        Returns
        -------
        sorted list of halfedges

        '''
        self.halfedge.sort(key=lambda a: a.angle, reverse=True)

class Edges:
    '''Edge of DCEL'''
    def __init__(self,point1,point2):
        self.prev = None
        self.next = None
        self.twin = None
        self.tail = point1
        self.face = None
        self.angle = findHAngle(point2.x-point1.x,point2.y-point1.y)
    
    def equivalence(self,_others):
        '''
        To check if edges are equivalent
        
        Parameters
        ----------
        _others : Edge
            

        Returns
        -------
        bool
            True if they are the same vertex and False if otherwise

        '''
        if self.tail == _others.tail and self.next.tail == _others.next.tail:
            return True
        else:
            return False
    
    def printedge(self):
        '''
        produce edges coefficients

        Returns
        -------
        self.tail.x, self.tail.y,self.next.tail.x,self.next.tail.y)
            if they exists

        '''
        if self.next !=None:
            return (self.tail.x, self.tail.y,self.next.tail.x,self.next.tail.y)
        else:
            return self.tail.x, self.tail.y

class Face:
    '''face of DCEL'''
    
    def __init__(self):
         self.halfEdge = None
         self.variable = None
   
class DCEL:
    '''Doubly Connected Edge List'''
    def __init__(self,vertexlist,edgelist):
        self.vertices = []
        self.edges = []
        self.faces = []
        self.vl = vertexlist
        self.el = edgelist
    
    def findVertex(self, x, y):
        '''
        locate vertex with x annd y coordinate

        Parameters
        ----------
        x : x coordinate

        y : y coordinate

        Returns
        -------
        vert : Vertex
            returns vertex with give x and y coordinates

        '''
        for vert in self.vertices:
            if vert.x == x and vert.y == y:
                return vert
        else:
            return None
    
    def findHalfEdge(self, v1, v2):
        '''
        find the half edge with vertices

        Parameters
        ----------
        v1 : First vertex

        v2 : Second Vertex


        Returns
        -------
        h : Half edge
            Half edge associated to the two given vertex

        '''
        for h in self.edges:
            nextEdge = h.next
            if (h.tail.x == v1[0] and h.tail.y == v1[1]) and (nextEdge.tail.x == v2[0] and nextEdge.tail.y == v2[1]):
                return h
        else:
            return None
    
    def printDCEL(self):
        '''
        generates DCEL with list of vertex and edges

        Returns
        -------
        DCEL 

        '''
        for v in self.vl:
            self.vertices.insert(-1,Vertex(v[0],v[1]))
        for e in self.el:
            start = e[0]
            end = e[1]
            if (start[0] and start[1]) >= 0 and (end[0] and end[1]) >= 0:
                v1 = self.findVertex(start[0], start[1])
                v2 = self.findVertex(end[0], end[1])
                e1 = Edges(v1,v2)
                e2 = Edges(v2,v1)
                e1.twin = e2
                e2.twin = e1
                v1.halfedge.append(e1)
                v2.halfedge.append(e2)
                self.edges.append(e1)
                self.edges.append(e2)
            
        for v in self.vertices:
            v.sortededges()
            halfedgecount = len(v.halfedge)
            if halfedgecount <2:
                return ("DCEL cannot be produced as it is invalid, it requires at least 2 half edge. Please try again.")
            else:
                for i in range(0, halfedgecount-1):
                    h1 = v.halfedge[i]
                    h2 = v.halfedge[i+1]
                    h1.twin.next = h2
                    h2.prev = h1.twin
                h1 = v.halfedge[halfedgecount-1]
                h2 = v.halfedge[0]
             
            indexface = 0
            newlist = self.edges[:]
            length = len(self.edges)
            while length > 0:
                he = newlist.pop()
                length-=1
                if he.face == None:
                    face = Face()
                    indexface += 1
                    face.halfedge = he
                    face.halfedge.faces = face
                while he.next != face.halfedge:
                    he = he.next
                    he.face = face
                self.faces.append(face)

           
    
    def findsection(self, section):
        '''
        finding a section

        Parameters
        ----------
        section : vertex


        Returns
        -------
        half edhe and start

        '''
        v1 = section[0]
        v2 = section[1]
        start = self.findHalfEdge(v1, v2)
        h = start
        while  h.next != start:
            print(h)
            h = h.next
        print(h, start)

vertex = [(0, 5), (2, 5), (3, 0), (0, 0)]
edge = [
      [(0, 5), (2, 5)],
      [(2, 5), (3, 0)],
      [(3, 0), (0, 0)],
      [(0, 0), (0, 5)],
      [(0, 5), (3, 0)],
  ]

dcel1 = DCEL(vertex,edge)
dcel1.printDCEL()     
dcel1.findsection([(3, 0), (0, 5)])      

class Room_Allocation(DCEL):
    def __init__(self,pathway_width):
        self.width = pathway_width
    def rooms(self,vertex,edge):
        '''
        Room alloaction using DCEL

        Parameters
        ----------
        vertex : Vertex
            list of vertices
        edge : Edge
            list of edges

        Returns
        -------
        dcel : DCEL
            return room allocation considering the width of pathway

        '''
        newedgelist = []
        for i in edge:
            for j in i:
                newedgelist.append((j[0]+self.width,j[1]))
        dcel = DCEL(vertex,newedgelist)
        dcel.printDCEL()     
        return dcel
        