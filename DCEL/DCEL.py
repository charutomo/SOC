# -*- coding: utf-8 -*-
"""
Created on Tue Mar 2 23:58:58 2021

@author: Charissa
"""
from Geometry.Vector import Vector

class Vertex(Vector):
    '''Vertex of DCEL'''
    def __init__(self, _x, _y):
        super().__init__(_x, _y)
        self.halfEdge = None

class HalfEdge:
    """HalfEdge
    
    Attributes
    ----------
    origin: Vector
        The point the edge starts from
    twin: HalfEdge
        The halfedge going in the opposite direction
    next: HalfEdge
        The next halfedge
    prev: HalfEdge
        The halfedge before this 
    """
    def __init__(self, _origin):
        self.origin = _origin
        self.twin = None
        self.incidentFace = None
        self.next = None
        self.prev = None

        self.destination = None
    
    def CreateTwin(self):
        if self.next is None:
            return None

        newHalfEdge = HalfEdge(self.next.origin)
        newHalfEdge.twin = self
        newHalfEdge.next = self.prev
        newHalfEdge.prev = self.next

        newHalfEdge.destination = self.origin
        self.destination = newHalfEdge.origin
        
        return newHalfEdge

    def __eq__(self, _other):
        '''
        To check if edges are equivalent
        
        Parameters
        ----------
        _other : HalfEdge

        Returns
        -------
        bool
            True if the origin and destination vertex are equal
        '''
        return self.origin == _other.origin and self.next.origin == _other.next.origin

    def Print(self):
        '''Prints edge coefficients

        Returns
        -------
            The origin of this halfedge and the origin of the next halfedge
        '''
        if self.next != None:
            return (self.origin.x, self.origin.y, self.next.origin.x, self.next.origin.y)
        else:
            return self.origin.x, self.origin.y

class Face:
    '''face of DCEL'''
    def __init__(self):
         self.halfEdge = None
   
class DCEL:
    '''Doubly Connected Edge List'''
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.faces = []