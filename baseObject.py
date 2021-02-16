import pygame

class BaseObject:
    def __init__(self, _left, _top):
        self.globalPosition = (_left, _top) # This is the top left position
        self.colour = pygame.Color(100, 100, 100)

    def Update(self):
        pass

    def Draw(self, _surface : pygame.Surface):
        pass
