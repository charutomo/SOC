import pygame
import random
from Geometry.Vector import Vector
from Geometry.Parabola import Parabola
from Rendering.Screen import Screen
from Voronoi.VoronoiGenerator import VoronoiGenerator
from DCEL.DCEL import DCEL
import Settings
import math

# Note that this is a linting error not a program error
# pylint: disable=no-member

# There might be a possible error if _x is 0
def GenerateRandomPoints(_length): #generate list of points, parameter how vetsors you want to generate
    points = [Vector] * _length
    for i in range(len(points)):
        points[i] = Vector(
            _x = random.random() * Settings.SCREEN_WIDTH,
            _y = random.random() * Settings.SCREEN_HEIGHT)
    return points
    
def GenerateFixedPoints():
    points = [Vector] * 3
    points[0] = Vector(50, 150)
    points[1] = Vector(125, 400)
    points[2] = Vector(350, 325)

    return points

def main():
    print("Main")

    points = GenerateRandomPoints(Settings.NUMBER_OF_POINTS)
    #points = GenerateFixedPoints()
    points.sort(key=lambda p: p.y)

    voronoiGenerator = VoronoiGenerator()
    dcel, circles, snapshots = voronoiGenerator.GenerateVoronoi(points)
    print(len(dcel.vertices), len(dcel.edges))

    pygame.init()
    screen = Screen()
    screen.points = points
    screen.circles = circles
    screen.snapshots = snapshots
    print(snapshots[1].Print())
    screen.dcel = dcel
    screen.Display(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
    screen.Update()
    
if __name__ == "__main__":
    main()
