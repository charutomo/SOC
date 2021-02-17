from enum import Enum
import random

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
NUMBER_OF_POINTS: int = 3

ID_LIST = list()

def GenerateUniqueID():
    while True:
        newID = random.randint(0, 9999)
        if newID not in ID_LIST:
            ID_LIST.append(newID)
            return newID