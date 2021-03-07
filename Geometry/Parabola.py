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
        return (1 / 2 * (self.focus.y - _directrix)) * ((_x - self.focus.x) ** 2) + ((self.focus.y + _directrix) / 2)

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
    def GetBreakpoint(_parabolaA, _parabolaB, _pointX):
        '''Gets the intersection between 2 parabolas

        Parameters
        ----------
        _parabolaA: Parabola
            The first parabola
        _parabolaB: Parabola
            The second parabola
        _point: Vector
            The point to check

        Returns
        -------
        The intersecting point as a Vector
        '''
        result = Vector(0.0, 0.0)
        p = _parabolaA.focus

        if _parabolaA.focus.x == _parabolaB.focus.x:
            result.y = (_parabolaA.focus.y + _parabolaB.focus.y) / 2
        elif _parabolaB.focus.x == _pointX:
            result.y = _parabolaB.focus.y
        elif _parabolaA.focus.x == _pointX:
            result.y = _parabolaA.focus.y
            p = _parabolaB.focus
        else:
            n0 = 2 * (_parabolaA.focus.x - _pointX)
            n1 = 2 * (_parabolaB.focus.x - _pointX)

            a = 1 / n0 - 1 / n1
            b = -2 * (_parabolaA.focus.y / n0 - _parabolaB.focus.y / n1)
            c = (_parabolaA.focus.y ** 2 + _parabolaA.focus.x ** 2 - _pointX ** 2) / n0 - (_parabolaB.focus.y ** 2 + _parabolaB.focus.x ** 2 - _pointX ** 2) / n1

            print("Parabola:", a, b, c)
            discriminant = b ** 2 - 4 * a * c
            if discriminant < 0: 
                return None
            result.y = (-b - math.sqrt(discriminant)) / (2*a)

        result.x = (p.x ** 2 + (p.y - result.y) ** 2 - _pointX ** 2) / (2 * p.x - 2 * _pointX)
        return result