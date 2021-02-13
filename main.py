import pygame
from VoronoiEvent import *
from screen import Screen

# Note that this is a linting error not a program error
# pylint: disable=no-member

def main():
    print("Main")

    sweepLine = 0.0
    points = [(10, 9), (100, 200), (50, 87), (150, 27)]
    queue = []

    points.sort(key=lambda p: p[1])

    for p in points:
        queue.append(SiteEvent(p))
    
    while len(queue) > 0:
        event = queue.pop()
        
        if event.type is EventType.SITEEVENT:
            event.HandleEvent(sweepLine)
        elif event.type is EventType.VERTEXEVENT:
            event.HandleEvent()

    #pygame.init()
    #screen = Screen()
    #screen.Display(640, 480)
    #screen.Update()
    
if __name__ == "__main__":
    main()
