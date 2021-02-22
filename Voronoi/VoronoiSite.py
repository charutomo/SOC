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

    def Print(self):
        """Prints the Vector"""
        print("Position: " + self.position.ToString())

