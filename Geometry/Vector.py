import math

class Vector:
    """Base 2D Object.
    
    Attributes
    ----------
    x: float
        The x coordinate
    y: float
        The y coordinate
    """
    def __init__(self, _x, _y):
        """Constructor 
        
        Parameters
        ----------
        _x: float
            The x coordinate
        _y: float
            The y coordinate
        """
        self.x = _x
        self.y = _y

    def __eq__(self, _other):
        """Equality Operator Override

        Override uses math.isclose for both x and y coordinates
        
        Parameters
        ----------
        _other: Vector
            The vector to compare to

        Returns
        -------
        A boolean value indicating whether the two vectors are approximately equal.
        Also returns False if _other is None
        """
        return math.isclose(self.x, _other.x) and math.isclose(self.y, _other.y)

    def ToTuple(self):
        """Converts and returns the Vector as a Tuple."""
        return (self.x, self.y)

    def ToString(self):
        """Converts and returns the Vector as a String."""
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def Print(self):
        """Prints the Vector"""
        print(self.ToString())

    # Static Methods

    @staticmethod
    def Midpoint(_vectorA, _vectorB):
        return Vector((_vectorA.x + _vectorB.x) / 2.0, (_vectorA.y + _vectorB.y) / 2.0)

    @staticmethod
    def EuclideanDistance(_vectorA, _vectorB):
        """Calculates the distance between 2 vectors
        
        Parameters
        ----------
        _vectorA: Vector
            The first vector to calculate with.
        _vectorB: Vector
            The second vector to calculate with.

        Returns
        -------
        Returns the distance as a float value.
        """
        
        return ((_vectorA.x - _vectorB.x) ** 2 + (_vectorA.y - _vectorB.y) ** 2) ** (1/2)