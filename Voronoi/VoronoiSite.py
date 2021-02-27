from Geometry.Vector import Vector

class VoronoiSite:
    """The origin point of a voronoi polygon.
    
    Attributes
    ----------
    position: Vector
        The position of the event
    """
    def __init__(self, _position):
        """Constructor 
        
        Parameters
        ----------
        _position: Vector
            The position of the event
        """
        self.position = _position

    def __eq__(self, _other):
        """Equality Operator Override

        Override uses vector equality
        
        Parameters
        ----------
        _other: Site
            The Site to compare to

        Returns
        -------
        A boolean value indicating whether the two sites are equal.
        """
        return self.position == _other.position

    def Print(self):
        """Prints the Vector"""
        print("Position: " + self.position.ToString())

