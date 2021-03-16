# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 22:00:23 2021

@author: Charissa
"""

from DCEL.DCEL import DCEL 

class Room(DCEL):
    def __init__(self,pathwaywidth):
        super().__init__()
        self.width = pathwaywidth
    def allocation(self):
        '''
        gives the room allocation considering the pathway widths

        Returns
        -------
        returns DCEL with the dimensions and division of the voronoi diagram

        '''
        for i in self.edges:
            self.edges += self.width 
        
        
        