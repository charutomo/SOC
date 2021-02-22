import math

class Parabola:
    """A curve made with a focus and a directrix.
    
    Attributes
    ----------
    focus: Vector
        The focus of the parabola
    """
    def __init__(self, _focus):
        """Constructor
        
        Parameters
        ----------
        _focus: Vector
            The focus of the parabola
        """
        self.focus = _focus

    def GetValue(self, _x: float, _directrix: float):
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
    def GetBreakpoint(_parabolaA, _parabolaB, _directrix):
        '''Gets the intersection between 2 parabolas

        Parameters
        ----------
        _parabolaA: Parabola
            The first parabola
        _parabolaB: Parabola
            The second parabola
        _directrix: float
            The current height of the directrix

        Returns
        -------
        The intersecting point as a Vector
        '''
        for x in range(640):        # Oh no what is this
            if math.isclose(_parabolaA.GetValue(x, _directrix), _parabolaB.GetValue(_parabolaB.x, _directrix)):
                return x, _parabolaA.GetValue(x,_directrix)
        return ("There are no intersection between the two parabolas.")