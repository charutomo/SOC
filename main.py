import pygame
import random
from vector import Vector
from screen import Screen
from voronoi import VoronoiGenerator

# Note that this is a linting error not a program error
# pylint: disable=no-member

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
NUMBER_OF_POINTS: int = 10

def GenerateRandomPoints(_length: int):
    points: [Vector] = [Vector] * _length
    for i in range(len(points)):
        points[i] = Vector(
            _x = random.random() * SCREEN_WIDTH,
            _y = random.random() * SCREEN_HEIGHT)
    return points

def main():
    print("Main")

    points: [Vector] = GenerateRandomPoints(NUMBER_OF_POINTS)
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
    screen.Display(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.Update()
    
if __name__ == "__main__":
    main()
