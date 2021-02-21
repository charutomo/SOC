import pygame.display
import Settings
from Vector import Vector
from Parabola import Parabola
from circumcircle import Circumcircle
from baseObject import BaseObject
from room import Room
from VoronoiSite import VoronoiSite

class Screen:
    def __init__(self):
        pygame.display.init()
        self.points: [Vector] = []
        self.vertices: [Vector] = []
        self.objects: [BaseObject] = []
        self.complete: bool = False
        self.clock: pygame.time.Clock = pygame.time.Clock()
    
    def Display(self, width : int, height : int):
        pygame.display.set_caption("Renderer")
        pygame.display.set_mode((width, height))

    def Draw(self):
        surface = pygame.display.get_surface()
        for o in self.objects:
            o.Draw(surface)
        for o in self.points:
            pygame.draw.ellipse(
                surface,
                pygame.Color(255, 0, 0),
                pygame.Rect(o.x, o.y, 4.0, 4.0))
        for v in self.vertices:
            pygame.draw.ellipse(
                surface,
                pygame.Color(0, 0, 255),
                pygame.Rect(v.x, v.y, 4.0, 4.0)
            )
        pygame.display.update()

    def Update(self):
        while not self.complete:
            for o in self.objects:
                o.Update()

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
                pygame.Color(255, 0, 0),
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

    