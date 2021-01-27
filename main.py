import pygame
from screen import Screen

# Note that this is a linting error not a program error
# pylint: disable=no-member

def main():
    print("Main")
    pygame.init()
    screen = Screen()
    screen.Display(640, 480)
    screen.Update()
    
if __name__ == "__main__":
    main()
