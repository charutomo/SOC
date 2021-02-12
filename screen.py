import pygame.display
from baseObject import BaseObject
from room import Room

class Screen:
    def __init__(self):
        pygame.display.init()
        self.objects = []
        self.complete = False
        self.clock = pygame.time.Clock()
    
    def Display(self, width : int, height : int):
        pygame.display.set_caption("Renderer")
        pygame.display.set_mode((width, height))

    def Draw(self):
        for o in self.objects:
            o.Draw(pygame.display.get_surface())
        pygame.display.update()

    def Update(self):
        while not self.complete:
            for o in self.objects:
                o.Update()

            self.Draw()

            self.clock.tick(60)


    