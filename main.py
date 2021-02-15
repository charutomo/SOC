import pygame
import random
from screen import Screen
from voronoi import VoronoiGenerator

# Note that this is a linting error not a program error
# pylint: disable=no-member

def main():
    print("Main")

    length = 5
    points = [None] * length
    for i in range(len(points)):
        points[i] = (random.random() * 640, random.random() * 480)
    points.sort(key=lambda p: p[1])
    
    voronoiGenerator = VoronoiGenerator()
    beachLine = voronoiGenerator.GenerateVoronoi(points)

    pygame.init()
    screen = Screen()
    for b in beachLine:
        screen.debugPoints.append(b.focus)
    screen.parabolas = beachLine
    screen.Display(640, 480)
    screen.Update()
    
if __name__ == "__main__":
    main()
