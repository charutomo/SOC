import math
from Geometry.Vector import Vector

class Parabola:
    """A curve made with a focus and a directrix.
    
    Attributes
    ----------
    focus: Vector
        The focus of the parabola
    """
    def __init__(self, _site):
        """Constructor
        
        Parameters
        ----------
        _focus: Vector
            The focus of the parabola
        """
        self.focus = _site

    def GetValue(self, _x, _directrix):
        """Computes the y value of the parabola given an x value.

        Reference: https://jacquesheunis.com/post/fortunes-algorithm/
        
        Parameters
        ----------
        _x: float
            The x coordinate 
        _directrix: float
            The current height of the directrix

        Returns
        -------
        The y coordinate as a float
        """

        return ((self.focus.x - _x) ** 2 + self.focus.y ** 2 - _directrix ** 2) / (2 * self.focus.y - 2 * _directrix)

    def ValidateParabola(self, _LHS, _RHS):
        """Checks if the length of the parabola is more than a threshold.

        Parameters
        ----------
        _LHS: Vector
            The LHS breakpoint
        _RHS: Vector
            The RHS breakpoint

        Returns
        -------
        Returns true if they are not close. False otherwise.
        """
        return _LHS != _RHS

    def Print(self):
        """Prints the Parabola"""
        print("Focus: " + self.focus.ToString())

    # Static Methods

    @staticmethod
    def get_breakpoint(site_a, site_b, directrix):
        '''Gets the intersection between 2 parabolas

        Parameters
        ----------
        _parabolaA: Parabola
            The first parabola
        _parabolaB: Parabola
            The second parabola
        _directrix: float
            The directrix (Sweepline)

        Returns
        -------
        The intersecting points as as Vector
        '''
        if site_a is None or site_b is None:
            return None

        if site_b.y == directrix:
            return site_b
        elif site_a.y == directrix:
            return site_a
        elif site_a.y == site_b.y:
            return Vector((site_a.x + site_b.x) / 2.0, site_a.y)
        else:
            a = Vector(site_a.x, site_a.y)
            b = Vector(site_b.x, site_b.y)
            c = directrix

            xSquaredCoefficient = b.y - a.y
            xCoefficient = 2 * (-a.x * b.y + a.x * c + b.x * a.y - b.x * c)
            constantA = b.y * (-(a.x ** 2) - (a.y ** 2) + c ** 2)
            constantB = a.y * (b.x ** 2 + b.y ** 2 - (c ** 2))
            constantC = c * (a.x ** 2 + a.y ** 2 - (b.x ** 2) - (b.y ** 2))
            constantValue = -(constantA + constantB + constantC)

            discriminant = xCoefficient ** 2 - 4 * xSquaredCoefficient * constantValue

            xA = (-xCoefficient - math.sqrt(discriminant)) / (2 * xSquaredCoefficient)
            yA = ((a.x - xA) ** 2 + a.y ** 2 - (c ** 2)) / (2 * (a.y - c))
            xB = (-xCoefficient + math.sqrt(discriminant)) / (2 * xSquaredCoefficient)
            yB = ((a.x - xB) ** 2 + a.y ** 2 - (c ** 2)) / (2 * (a.y - c))

            if xB > site_a.x and xB < site_b.x:
                return Vector(xB, yB)
            else:
                return Vector(xA, yA)