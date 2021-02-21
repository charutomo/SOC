from enum import Enum
import random

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
NUMBER_OF_POINTS: int = 6

POINT_WIDTH: float = 4.0
CIRCLE_BORDER_WIDTH: float = 1.0

ID_LIST = list()

def GenerateUniqueID():
    while True:
        newID = random.randint(0, 9999)
        if newID not in ID_LIST:
            ID_LIST.append(newID)
            return newID