# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 21:14:32 2021

@author: Charissa
"""

def circumcircle(x1,y1,x2,y2,x3,y3):
    '''
    Parameters 
    ----------
    x1 : float
        coefficient of first x coordinate
    y1 : float
        coefficient of first y coordinate
    x2 : float
        coefficient of second x coordinate
    y2 : float
        coefficient of second y coordinate
    x3 : float
        coefficient of third x coordinate
    y3 : float
        coefficient of third y coordinate

    Returns
    -------
    (x, y): tuple
        center point of the circle
    
    r : float
        radius of the circle passing through 3 points (x1,y1),(x2,y2),(x3,y3)

    ''' # use docstring so can have help option on function 
    
    A = x1*(y2-y3)-y1*(x2-x3)+x2*y3-x3*y2
    B = (x1**2 +y1**2)*(y3-y2) + (x2**2+y2**2)*(y1-y3) + (x3**2+y3**2)*(y2-y1)
    C = (x1**2+y1**2)*(x2-x3)+(x2**2+y2**2)*(x3-x1)+(x3**2+y3**2)*(x1-x2)
    D = (x1**2+y1**2)*(x3*y2-x2*y3)+(x2**2+y2**2)*(x1*y3-x3*y1)+(x3**2+y3**2)*(x2*y1-x1*y2)
    x = -B/(2*A)
    y = -C/(2*A)
    r = ((B**2+C**2-4*A*D)/(4*A**2))**1/2 
    
    #Alternate Formula (if you want to use, I have checked that it will give same answer)
    #x = ((x1**2+y1**2)*(y2-y3)+(x2**2+y2**2)*(y3-y1)+(x3**2+y3**2)*(y1-y2))/(2*(x1*(y2-y3)-y1*(x2-x3)+x2*y3-x3*y2))
    #y = ((x1**2+y1**2)*(x3-x2)+(x2**2+y2**2)*(x1-x3)+(x3**2+y3**2)*(x2-x1))/(2*(x1*(y2-y3)-y1*(x2-x3)+x2*y3-x3*y2))
    #r = ((x-x1)**2 +(y-y1)**2)**1/2 
    return (x,y) , r
print(circumcircle(1,7,4,2,5,9)) #an example
    

