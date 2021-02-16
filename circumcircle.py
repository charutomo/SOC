import pygame
from vector import Vector

class Circumcircle:
    def __init__(self, _a: Vector, _b: Vector, _c: Vector):
        self.a = _a
        self.b = _b
        self.c = _c
        self.midpoint = None
        self.radius = None
        self.lowestPoint = None
        
    def Generate(self):
        '''
        Parameters 
        ----------
        _a.x : float
            coefficient of first x coordinate
        _a.y : float
            coefficient of first y coordinate
        _b.x : float
            coefficient of second x coordinate
        _b.y : float
            coefficient of second y coordinate
        _c.x : float
            coefficient of third x coordinate
        _c.y : float
            coefficient of third y coordinate

        Returns
        -------
        (x, y): Vector
            center point of the circle
        
        r : float
            radius of the circle passing through 3 points (self.a.x,self.a.y),(self.b.x,self.b.y),(self.c.x,self.c.y)

        ''' # use docstring so can have help option on function 
        
        #A = self.a.x*(self.b.y-self.c.y)-self.a.y*(self.b.x-self.c.x)+self.b.x*self.c.y-self.c.x*self.b.y
        #B = (self.a.x**2 +self.a.y**2)*(self.c.y-self.b.y) + (self.b.x**2+self.b.y**2)*(self.a.y-self.c.y) + (self.c.x**2+self.c.y**2)*(self.b.y-self.a.y)
        #C = (self.a.x**2+self.a.y**2)*(self.b.x-self.c.x)+(self.b.x**2+self.b.y**2)*(self.c.x-self.a.x)+(self.c.x**2+self.c.y**2)*(self.a.x-self.b.x)
        #D = (self.a.x**2+self.a.y**2)*(self.c.x*self.b.y-self.b.x*self.c.y)+(self.b.x**2+self.b.y**2)*(self.a.x*self.c.y-self.c.x*self.a.y)+(self.c.x**2+self.c.y**2)*(self.b.x*self.a.y-self.a.x*self.b.y)
        #x = -B/(2*A)
        #y = -C/(2*A)
        #r = ((B**2+C**2-4*A*D)/(4*A**2))**(1/2) 
        
        #Alternate Formula (if you want to use, I have checked that it will give same answer)
        x = ((self.a.x**2+self.a.y**2)*(self.b.y-self.c.y)+(self.b.x**2+self.b.y**2)*(self.c.y-self.a.y)+(self.c.x**2+self.c.y**2)*(self.a.y-self.b.y))/(2*(self.a.x*(self.b.y-self.c.y)-self.a.y*(self.b.x-self.c.x)+self.b.x*self.c.y-self.c.x*self.b.y))
        y = ((self.a.x**2+self.a.y**2)*(self.c.x-self.b.x)+(self.b.x**2+self.b.y**2)*(self.a.x-self.c.x)+(self.c.x**2+self.c.y**2)*(self.b.x-self.a.x))/(2*(self.a.x*(self.b.y-self.c.y)-self.a.y*(self.b.x-self.c.x)+self.b.x*self.c.y-self.c.x*self.b.y))
        r = ((x-self.a.x)**2 + (y-self.a.y)**2)**(1/2) 
        
        self.midpoint = Vector(x,y)
        self.radius = r

        self.lowestPoint = Vector(self.midpoint.x, self.midpoint.y + r)
    
    def Draw(self, _surface: pygame.surface.Surface, _color: pygame.Color = pygame.Color(0, 255, 0), _ellipseBox: Vector = Vector(4.0, 4.0), _circleBorderWidth: int = 1):
        pygame.draw.ellipse(
            pygame.display.get_surface(),
            _color,
            pygame.Rect(self.midpoint.x, self.midpoint.y, _ellipseBox.x, _ellipseBox.y)
        )
        pygame.draw.line(
            pygame.display.get_surface(),
            _color,
            self.midpoint.ToTuple(),
            self.lowestPoint.ToTuple()
        )
        pygame.draw.circle(
            pygame.display.get_surface(),
            _color,
            self.midpoint.ToTuple(),
            self.radius,
            _circleBorderWidth
        )

    def Print(self):
        print("*********************************")
        print("Vector A: " + self.a.ToString() \
            + "\nVector B: " + self.b.ToString() \
            + "\nVector C: " + self.c.ToString() \
            + "\nMidpoint: " + self.midpoint.ToString() \
            + "\nRadius: " + str(self.radius) \
            + "\nLowest Point: " + self.lowestPoint.ToString())
        print("*********************************")