import pygame
from baseObject import BaseObject

class Room(BaseObject):
    def __init__(self, _left, _top, _width, _height, _thickness):
        super().__init__(_left = _left, _top = _top)
        self.width = _width
        self.height = _height
        self.thickness = _thickness

    def Draw(self, _surface : pygame.Surface):
        pygame.draw.rect(
            surface = _surface, 
            color = self.colour, 
            rect = pygame.Rect(self.globalPosition[0], self.globalPosition[1], self.width, self.height),
            width = self.thickness
        )


