import pygame.display
from vector import Vector
from parabola import Parabola
from circumcircle import Circumcircle
from baseObject import BaseObject
from room import Room

class Screen:
    def __init__(self):
        pygame.display.init()
        self.debugPoints: [Vector] = []
        self.parabolas: [Parabola] = []
        self.sweepLine: float = None
        self.circumcircles: [Circumcircle] = [] 
        self.consideredCircumcircles: [Circumcircle] = []
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
        for o in self.debugPoints:
            pygame.draw.ellipse(
                surface,
                pygame.Color(255, 0, 0),
                pygame.Rect(o.x, o.y, 4.0, 4.0))
        """
        for p in self.parabolas:
            p.Draw(surface, 1000, 0.25, self.sweepLine)
        """
        """
        for c in self.circumcircles:
            c.Draw(surface)
        """
        for c in self.consideredCircumcircles:
            c.Draw(surface, pygame.Color(0, 125, 125))
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


    