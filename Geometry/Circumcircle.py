from Geometry.Vector import Vector

class Circumcircle:
    """
    The circumcircle object made from three vectors

    Attributes
    ----------
    vectorA: Vector
        The first vector
    vectorB: Vector
        The second vector
    vectorC: Vector
        The third vector
    midpoint: Vector
        The midpoint of the circle
    radius: float
        The radius of the circle
    lowestPoint: Vector
        The point on the boundary of the circle with the smallest y value
    """
    def __init__(self, _vectorA: Vector, _vectorB: Vector, _vectorC: Vector):
        """Constructor
        
        Parameters
        ----------
        _vectorA: Vector
            The first vector
        _vectorB: Vector
            The second vector
        _vectorC: Vector
            The third vector
        """
        self.vectorA = _vectorA
        self.vectorB = _vectorB
        self.vectorC = _vectorC
        self.midpoint = None
        self.radius = None
        self.lowestPoint = None
        
    def Generate(self):
        '''Calculates the midpoint, radius, and lowestPoint of the circumcircle.'''
        a = self.vectorA
        b = self.vectorB
        c = self.vectorC
        x = ((a.x**2+a.y**2)*(b.y-c.y)+(b.x**2+b.y**2)*(c.y-a.y)+(c.x**2+c.y**2)*(a.y-b.y))/(2*(a.x*(b.y-c.y)-a.y*(b.x-c.x)+b.x*c.y-c.x*b.y))
        y = ((a.x**2+a.y**2)*(c.x-b.x)+(b.x**2+b.y**2)*(a.x-c.x)+(c.x**2+c.y**2)*(b.x-a.x))/(2*(a.x*(b.y-c.y)-a.y*(b.x-c.x)+b.x*c.y-c.x*b.y))
        r = ((x-a.x)**2 + (y-a.y)**2)**(1/2) 
        
        self.midpoint = Vector(x,y)
        self.radius = r
        self.lowestPoint = Vector(self.midpoint.x, self.midpoint.y + r)

    def Print(self):
        """Prints the circumcircle."""
        print("*********************************")
        print("Vector A: " + self.vectorA.ToString() \
            + "\nVector B: " + self.vectorB.ToString() \
            + "\nVector C: " + self.vectorC.ToString() \
            + "\nMidpoint: " + self.midpoint.ToString() \
            + "\nRadius: " + str(self.radius) \
            + "\nLowest Point: " + self.lowestPoint.ToString())
        print("*********************************")
    
    # Static Methods

    @staticmethod
    def InCircle(_circumcircle, _vector):
        """Determines if the given Vector lies within the circle
        
        Parameters
        ----------
        _circumcircle: Circumcircle
            The circumcircle to check
        _vector: Vector
            The vector to check

        Returns
        -------
        Returns a boolean value
        """
        return Vector.EuclideanDistance(_circumcircle.midpoint, _vector) <= _circumcircle.radius

    @staticmethod
    def NoneInCircle(_circumcircle, _vectors):
        """Determines if any of the given Vectors lies within the circle
        
        Parameters
        ----------
        _circumcircle: Circumcircle
            The circumcircle to check
        _vectors: [Vector]
            The vectors to check

        Returns
        -------
        Returns a boolean value 
        """
        for v in _vectors:
            if v != _circumcircle.vectorA and v != _circumcircle.vectorB and v != _circumcircle.vectorC and Circumcircle.InCircle(_circumcircle, v):
                return False
        
        return True