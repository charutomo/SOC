import pygame.display
import math
import Settings
from Geometry.Vector import Vector
from Geometry.Parabola import Parabola

class Screen:
    """Renderer
    
    Attributes
    ----------
    complete: Boolean
        Whether the renderer should stop updating
    clock: Clock
        The clock used to update
    """
    def __init__(self):
        """Constructor"""
        pygame.display.init()
        self.points = []
        self.vertices = []
        self.halfEdges = []
        self.rootArc = None
        self.complete = False
        self.clock = pygame.time.Clock()
    
    def Display(self, _width, _height, _caption = "Renderer"):
        """Display Function

        Parameters
        ----------
        _width: float
            The horizontal length of the screen
        _height: float
            The vertical length of the screen
        _caption: String
            The window title
        """
        pygame.display.set_mode((_width, _height))
        pygame.display.set_caption(_caption)

    def Draw(self):
        """Draw Function"""
        surface = pygame.display.get_surface()
        
        for o in self.points:
            pygame.draw.ellipse(
                surface,
                pygame.Color(255, 0, 0),
                pygame.Rect(o.x, o.y, 4.0, 4.0))
        
        for e in self.halfEdges:
            pygame.draw.line(
                surface,
                pygame.Color(0, 255, 0),
                e.origin.ToTuple(), 
                e.twin.origin.ToTuple(), 
                1)
                
        pygame.display.update()

    def Update(self):
        """Update Function"""
        while not self.complete:
            self.Draw()

            self.clock.tick(60)

    def DrawParabola(self, _parabola, _surface, _resolution, _increment, _directrix):
        '''Draws the parabola onto a pygame surface

        Parameters
        ----------
        _parabola: Parabola
            The parabola to draw
        _surface: Surface
            The surface to draw on
        _resolution: int
            The number of points to draw
        _increment: float
            The horizontal difference between each drawn coordinate
        _directrix: float
            The current height of the directrix
        '''
        xPos = _parabola.focus.x - (math.floor(_resolution / 2) * _increment)
        for i in range(_resolution):
            pygame.draw.line(
                _surface,
                pygame.Color(125, 125, 0),
                (xPos, _parabola.GetValue(xPos, _directrix)),
                (xPos + _increment, _parabola.GetValue(xPos + _increment, _directrix)))
            xPos += _increment

    def DrawCircle(self, _circle, _surface, _color = pygame.Color(0, 255, 0)):
        '''Draws the circumcircle onto a pygame surface

        Parameters
        ----------
        _circle: Circle
            The circle to draw
        _surface: Surface
            The surface to draw on
        _color: Color, Optional
            The color of the circle
        '''
        pygame.draw.ellipse(
            pygame.display.get_surface(),
            _color,
            pygame.Rect(_circle.midpoint.x, _circle.midpoint.y, Settings.POINT_WIDTH, Settings.POINT_WIDTH)
        )
        pygame.draw.line(
            pygame.display.get_surface(),
            _color,
            _circle.midpoint.ToTuple(),
            _circle.lowestPoint.ToTuple()
        )
        pygame.draw.circle(
            pygame.display.get_surface(),
            _color,
            _circle.midpoint.ToTuple(),
            _circle.radius,
            Settings.CIRCLE_BORDER_WIDTH
        )

    