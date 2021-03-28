import math
import random
import pygame
from Geometry.Vector import Vector
from Rendering.Screen import Screen
from Voronoi.VoronoiGenerator import VoronoiGenerator
import Settings

# Note that this is a linting error not a program error
# pylint: disable=no-member

# There might be a possible error if _x is 0
def GenerateRandomPoints(_length): #generate list of points, parameter how vetsors you want to generate
    points = [Vector] * _length
    for i in range(len(points)):
        points[i] = Vector(
            _x = math.floor(random.random() * Settings.SCREEN_WIDTH),
            _y = math.floor(random.random() * Settings.SCREEN_HEIGHT))
    return points
    
def GenerateFixedPoints():
    points = [Vector] * 3
    points[0] = Vector(50, 150)
    points[1] = Vector(125, 400)
    points[2] = Vector(350, 325)

    return points

def main():
    print("Main")

    #points = GenerateRandomPoints(Settings.NUMBER_OF_POINTS)
    points = GenerateFixedPoints()
    points.sort(key=lambda p: p.y)

    voronoi_generator = VoronoiGenerator(points)

    pygame.init()
    screen = Screen(voronoi_generator)
    screen.voronoi_painter.run()
    screen.display(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
    screen.update()

if __name__ == "__main__":
    main()
