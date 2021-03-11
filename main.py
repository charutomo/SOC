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

def GenerateRandomPoints(_length): #generate list of points, parameter how vetsors you want to generate
    points = [Vector] * _length
    for i in range(len(points)):
        points[i] = Vector(
            _x = math.floor(random.random() * Settings.SCREEN_WIDTH),
            _y = math.floor(random.random() * Settings.SCREEN_HEIGHT))
    return points
    
def main():
    print("Main")

    points = GenerateRandomPoints(Settings.NUMBER_OF_POINTS)
    points.sort(key=lambda p: p.y)

    voronoiGenerator = VoronoiGenerator()
    dcel = voronoiGenerator.GenerateVoronoi(points)
    print(len(dcel.vertices), len(dcel.edges))

    pygame.init()
    screen = Screen()
    screen.points = points
    screen.dcel = dcel
    screen.Display(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
    screen.Update()
    
if __name__ == "__main__":
    main()
