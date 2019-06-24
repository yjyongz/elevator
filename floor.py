import threading
from enum import Enum

class Door(Enum):
    CLOSE = 0
    OPEN = 1

class Direction(Enum):
    UP = 0
    DOWN = 1
    NONE = -1

class Firstfloor:
    def __init__(self, floor, direction):
        self.floor = floor
        self.updirection = direction
        self.hasStop = 0
        self.door = Door.CLOSE

class Lastfloor:
    def __init__(self, floor, direction):
        self.floor = floor
        self.downdirection = direction
        self.hasStop = 0
        self.door = Door.CLOSE

class Floor:
    def __init__(self, floor, updirection, downdirection):
        self.floor = floor
        self.updirection = updirection
        self.downdirection = downdirection
        self.downhasStop = 0
        self.uphasStop = 0
        self.door = Door.CLOSE
