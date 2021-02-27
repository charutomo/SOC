from enum import Enum

class EventType(Enum):
    """Event Type
    
    The types of events that the voronoi algorithm handles
    """
    SITEEVENT = 1
    VERTEXEVENT = 2

class VoronoiEvent:
    """Base Event Class.
    
    Attributes
    ----------
    position: Vector
        The position of the event
    type: EventType
        The kind of event
    """
    def __init__(self, _position, _type):
        """Constructor 
        
        Parameters
        ----------
        _position: Vector
            The position of the event
        _type: EventType
            The kind of event
        """
        self.position = _position
        self.type = _type
    
    def HandleEvent(self):
        """Event Trigger."""
        pass

class SiteEvent(VoronoiEvent):
    """Site Event.

    A site event is created when the sweepline passes through a site.\n
    A parabola is created with the site as the focus and the sweepline as the directrix.\n
    Finally, the program will iterate through triplets of sites to construct circumcircle events.
    
    Attributes
    ----------
    site: Vector
        The site that triggers the event
    """
    def __init__(self, _site):
        """Constructor 
        
        Parameters
        ----------
        _site: Vector
            The site that triggers the event
        """
        super().__init__(_site, EventType.SITEEVENT)
        self.site = _site
    
    def HandleEvent(self):
        """Site Event Trigger.

        Returns
        -------
        The site that the sweepline passes through 
        """
        return self.site

class CircleEvent(VoronoiEvent):
    """Circle Event.

    A circle event is created when the sweepline passes through the lowest point on a circumcircle.\n
    The associated parabola will be deleted and the midpoint of the circumcircle is added to the vertex list.
    
    Attributes
    ----------
    circumcircle: Circumcircle
        The bounding circumcircle 
    """
    def __init__(self, _circumcircle):
        """Constructor 
        
        Parameters
        ----------
        _circumcircle: Circumcircle
            The bounding circumcircle 
        """
        super().__init__(_circumcircle.lowestPoint, EventType.VERTEXEVENT)
        self.circumcircle = _circumcircle

    def HandleEvent(self):
        """Circle Event Trigger.

        Returns
        -------
        The circumcircle that contains the lowest point
        """
        return self.circumcircle

