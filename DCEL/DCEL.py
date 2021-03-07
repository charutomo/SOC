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
    incidentFace: Face
        The face to the left of the halfedge
    next: HalfEdge
        The next halfedge
    prev: HalfEdge
        The halfedge before this 
    """
    def __init__(self, _origin):
        self.origin = _origin
        self.destination = None
        self.twin = None
        self.incidentFace = None
        self.next = None
        self.prev = None
    
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
        if _other == None or _other.origin == None or _other.next.origin == None: return
        return self.origin == _other.origin and self.next.origin == _other.next.origin
    
    def Complete(self, _endPoint):
        self.destination = _endPoint

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

class Edge:
    """Edge

    An edge is two opposing half edges
    
    Attributes
    ----------
    _rightHalfEdge: HalfEdge
        The rightHalfEdge
    _leftHalfEdge: HalfEdge
        The leftHalfEdge
    """
    def __init__(self, _rightHalfEdge, _leftHalfEdge):
        self.rightHalfEdge = _rightHalfEdge
        self.leftHalfEdge = _leftHalfEdge

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