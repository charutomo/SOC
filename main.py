import pygame
import random
from Geometry.Vector import Vector
from Rendering.Screen import Screen
from Voronoi.VoronoiGenerator import VoronoiGenerator
import Settings

# Note that this is a linting error not a program error
# pylint: disable=no-member

def GenerateRandomPoints(_length: int): #generate list of points, parameter how vetsors you want to generate
    points: [Vector] = [Vector] * _length
    for i in range(len(points)):
        points[i] = Vector(
            _x = random.random() * Settings.SCREEN_WIDTH,
            _y = random.random() * Settings.SCREEN_HEIGHT)
    return points

def main():
    print("Main")

    points = GenerateRandomPoints(Settings.NUMBER_OF_POINTS)
    points.sort(key=lambda p: p.y)

    voronoiGenerator = VoronoiGenerator()
    vertices = voronoiGenerator.GenerateVoronoi(points)

    pygame.init()
    screen = Screen()
    screen.points = points
    screen.vertices = vertices
    screen.Display(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
    screen.Update()
    
if __name__ == "__main__":
    main()
