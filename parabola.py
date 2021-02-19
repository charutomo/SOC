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
        '''
        Parameters
        ----------
        _other : class
            inputs of the other parabola
        _sweepLine : float
            the y-axis of the sweepline

        Returns
        -------
        x, y position of the intersections of the parabola
            
        '''
        for x in range(640):
            if  self.GetYValue(self,x,_sweepLine) == _other.GetYValue(_other,x,_sweepLine):
                return x , self.GetYValue(x,_sweepLine)
        return ("There are no intersection between the two parabolas.")

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

    