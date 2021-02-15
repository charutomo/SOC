import pygame.display
from vector import Vector
from parabola import Parabola
from baseObject import BaseObject
from room import Room

class Screen:
    def __init__(self):
        pygame.display.init()
        self.debugPoints: [Vector] = []
        self.parabolas: [Parabola] = []
        self.sweepLine: float = None
        self.objects: [BaseObject] = []
        self.complete: bool = False
        self.clock: pygame.time.Clock = pygame.time.Clock()
    
    def Display(self, width : int, height : int):
        pygame.display.set_caption("Renderer")
        pygame.display.set_mode((width, height))

    def Draw(self):
        for o in self.objects:
            o.Draw(pygame.display.get_surface())
        for o in self.debugPoints:
            pygame.draw.ellipse(
                pygame.display.get_surface(),
                pygame.Color(255, 0, 0),
                pygame.Rect(o.x, o.y, 4.0, 4.0))
        for p in self.parabolas:
            p.Draw(pygame.display.get_surface(), 1000, 0.25, self.sweepLine)
        pygame.display.update()

    def Update(self):
        while not self.complete:
            for o in self.objects:
                o.Update()

            self.Draw()

            self.clock.tick(60)


    