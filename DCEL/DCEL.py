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
    def __init__(self, _origin, _edges):
        self.origin = _origin
        self.twin = None
        self.incidentFace = None
        self.next = None
        self.prev = None

        _edges.append(self)

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
        if self.next is None and _other.next is not None: return False
        elif self.next is not None and _other.next is None: return False
        elif self.next is None and _other.next is None: return self.origin == _other.origin
        else: return self.origin == _other.origin and self.next.origin == _other.next.origin

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
    def __init__(self, _vertices, _edges, _faces):
        self.vertices = _vertices
        self.edges = _edges
        self.faces = _faces