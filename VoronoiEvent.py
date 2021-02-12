from enum import Enum
from parabola import Parabola

class EventType(Enum):
    SITEEVENT = 1
    VERTEXEVENT = 2

# A circumcircle is created when you can choose 3 points (the middle of which is the newest point generated from the point event)
# A circle event is triggered when the sweep line touches the bottom most point of the circumcircle and all 3 points and the sweep line are equidistant from the center
# I believe, the 3 points chosen are based on the parabola list. So if it cuts a parabola into 2, then it takes itself, the cut parabola, and either the right or left parabola
# More than 1 circle can be formed

class VoronoiEvent:
    def __init__(self, _position : (float, float), _type : EventType):
        self.position = _position
        self.type = _type
    
    def HandleEvent(self):
        pass

class SiteEvent(VoronoiEvent):
    def __init__(self, _position : (float, float)):
        super.__init__(_position, EventType.SITEEVENT)
    
    def HandleEvent(self, _sweepLineHeight : float):
        return Parabola(self.position, _sweepLineHeight)

class CircleEvent(VoronoiEvent):
    def __init__(self, _position : (float, float)):
        super.__init__(_position, EventType.VERTEXEVENT)

    def HandleEvent(self):
        pass

