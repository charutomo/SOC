import pygame
from vector import Vector
from VoronoiSite import VoronoiSite

class Circumcircle:
    def __init__(self, _associatedSite: VoronoiSite, _siteA: VoronoiSite, _siteB: VoronoiSite, _siteC: VoronoiSite):
        self.associatedSite: VoronoiSite = _associatedSite
        self.siteA: VoronoiSite = _siteA
        self.siteB: VoronoiSite = _siteB
        self.siteC: VoronoiSite = _siteC
        self.midpoint: Vector = None
        self.radius: float = None
        self.lowestPoint: Vector = None
        
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
        a = self.siteA.position
        b = self.siteB.position
        c = self.siteC.position
        x = ((a.x**2+a.y**2)*(b.y-c.y)+(b.x**2+b.y**2)*(c.y-a.y)+(c.x**2+c.y**2)*(a.y-b.y))/(2*(a.x*(b.y-c.y)-a.y*(b.x-c.x)+b.x*c.y-c.x*b.y))
        y = ((a.x**2+a.y**2)*(c.x-b.x)+(b.x**2+b.y**2)*(a.x-c.x)+(c.x**2+c.y**2)*(b.x-a.x))/(2*(a.x*(b.y-c.y)-a.y*(b.x-c.x)+b.x*c.y-c.x*b.y))
        r = ((x-a.x)**2 + (y-a.y)**2)**(1/2) 
        
        self.midpoint = Vector(x,y)
        self.radius = r

        self.lowestPoint = Vector(self.midpoint.x, self.midpoint.y + r)
    
    def InCircle(self, _site: VoronoiSite):
        dist = self.midpoint.EuclideanDistance(_site.position)
        return dist <= self.radius

    def NoneInCircle(self, _sites: [VoronoiSite]):
        for s in _sites:
            if s != self.siteA and s != self.siteB and s != self.siteC and self.InCircle(s):
                return False
        
        return True

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
        print("Vector A: " + self.siteA.ToString() \
            + "\nVector B: " + self.siteB.ToString() \
            + "\nVector C: " + self.siteC.ToString() \
            + "\nMidpoint: " + self.midpoint.ToString() \
            + "\nRadius: " + str(self.radius) \
            + "\nLowest Point: " + self.lowestPoint.ToString())
        print("*********************************")