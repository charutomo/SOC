import pygame
import random
from vector import Vector
from screen import Screen
from voronoi import VoronoiGenerator
import Settings

# Note that this is a linting error not a program error
# pylint: disable=no-member


def GenerateRandomPoints(_length: int):
    points: [Vector] = [Vector] * _length
    for i in range(len(points)):
        points[i] = Vector(
            _x = random.random() * Settings.SCREEN_WIDTH,
            _y = random.random() * Settings.SCREEN_HEIGHT)
    return points

def main():
    print("Main")

    points: [Vector] = GenerateRandomPoints(Settings.NUMBER_OF_POINTS)
    points.sort(key=lambda p: p.y)
    
    voronoiGenerator = VoronoiGenerator()
    beachLine, sweepLine, circumcircles, vertices = voronoiGenerator.GenerateVoronoi(points)

    pygame.init()
    screen = Screen()
    for b in beachLine:
        screen.debugPoints.append(b.focus)
    screen.parabolas = beachLine
    screen.sweepLine = sweepLine
    screen.circumcircles = circumcircles
    screen.vertices = vertices
    screen.Display(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
    screen.Update()
    
if __name__ == "__main__":
    main()
