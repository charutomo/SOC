import math
import pygame

class Parabola:
    def __init__(self, _focus, _directrix):
        self.focus = _focus
        self.directrix = _directrix
        self.origin = self.focus[1] - self.directrix

    # Get the x value of a parabola given the y value
    # Note that x has to be bounded withn the range
    def GetYValue(self, _x):
        return (math.pow(_x - self.focus[0], 2) + self.focus[1])

    def Draw(self, _surface, _resolution, _increment):
        xPos = self.focus[0] - (math.floor(_resolution / 2) * _increment)
        for i in range(_resolution):
            pygame.draw.line(
                _surface,
                pygame.Color(255, 0, 0),
                (xPos, self.GetYValue(xPos)),
                (xPos + _increment, self.GetYValue(xPos + _increment)))
            xPos += _increment

    def Print(self):
        print("Focus: " + str(self.focus) + ", Directrix: " + str(self.directrix))

    