import pygame

class BaseObject:
    def __init__(self, _left, _top):
        self.globalPosition = (_left, _top) # This is the top left position
        self.colour = pygame.Color(red = 100, green = 100, blue = 100)

    def Update(self):
        pass

    def Draw(self, _surface : pygame.Surface):
        pass
