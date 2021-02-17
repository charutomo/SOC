import math
import pygame
import Settings
from vector import Vector

class Parabola:
    def __init__(self, _focus: Vector):
        self.focus = _focus

    def GetYValue(self, _x: float, _directrix: float):
        return (-math.pow(_x - self.focus.x, 2) / 4 * _directrix + self.focus.y)

    # Get the intersection of 2 parabolas
    def GetBreakpoint(self, _other, _sweepLine: float):
        pass

    def Copy(self):
        return Parabola(self.focus)

    def Draw(self, _surface: pygame.surface.Surface, _resolution: int, _increment: float, _directrix: float):
        xPos = self.focus.x - (math.floor(_resolution / 2) * _increment)
        for i in range(_resolution):
            pygame.draw.line(
                _surface,
                pygame.Color(255, 0, 0),
                (xPos, self.GetYValue(xPos, _directrix)),
                (xPos + _increment, self.GetYValue(xPos + _increment, _directrix)))
            xPos += _increment

    def Print(self):
        print("Focus: " + self.focus.ToString())

    