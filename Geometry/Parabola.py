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
    def GetBreakpoint(_parabolaA, _parabolaB, _directrix, _leftIntersection):
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
        The intersecting point as a Vector
        '''
        result = Vector(0.0, 0.0)

        if _parabolaB.focus.y == _directrix:
            return _parabolaB.focus
        elif _parabolaA.focus.y == _directrix:
            return _parabolaA.focus
        else:
            a = Vector(_parabolaA.focus.x, _parabolaA.focus.y)
            b = Vector(_parabolaB.focus.x, _parabolaB.focus.y)
            c = _directrix

            xSquaredCoefficient = b.y - a.y
            xCoefficient = 2 * (-a.x * b.y + a.x * c + b.x * a.y - b.x * c)
            constantA = b.y * (-(a.x ** 2) - (a.y ** 2) + c ** 2)
            constantB = a.y * (b.x ** 2 + b.y ** 2 - (c ** 2))
            constantC = c * (a.x ** 2 + a.y ** 2 - (b.x ** 2) - (b.y ** 2))
            constantValue = -(constantA + constantB + constantC)

            discriminant = xCoefficient ** 2 - 4 * xSquaredCoefficient * constantValue

            xA = (-xCoefficient + math.sqrt(discriminant)) / (2 * xSquaredCoefficient)
            xB = (-xCoefficient - math.sqrt(discriminant)) / (2 * xSquaredCoefficient)

            chosenValue = xB
            if _leftIntersection:
                if xA < xB:
                    chosenValue = xA
            else:
                if xA > xB:
                    chosenValue = xA

            result.x = chosenValue
            result.y = ((a.x - result.x) ** 2 + a.y ** 2 - (c ** 2)) / (2 * (a.y - c))
            return result