import pygame
from screen import Screen
from voronoi import VoronoiGenerator

# Note that this is a linting error not a program error
# pylint: disable=no-member

def main():
    print("Main")

    generator = VoronoiGenerator()
    generator.GenerateVoronoi({(10, 10), (45, 50), (69, 100)})

    pygame.init()
    screen = Screen()
    screen.Display(640, 480)
    screen.Update()
    
if __name__ == "__main__":
    main()
