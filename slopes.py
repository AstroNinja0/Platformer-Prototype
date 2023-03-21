import pygame
from enum import Enum, auto

class SlopeType(Enum):
    Empty = auto()
    Block = auto()
    OneWay = auto()

    TestSlopeMid1 = auto()
    TestSlopeMid1FX = auto()
    TestSlopeMid1FY = auto()
    TestSlopeMid1FXY = auto()
    TestSlopeMid1F90 = auto()
    TestSlopeMid1F90X = auto()
    TestSlopeMid1F90Y = auto()
    TestSlopeMid1F90XY = auto()

    TestSlope45 = auto()
    TestSlope45FX = auto()
    TestSlope45FY = auto()
    TestSlope45FXY = auto()
    TestSlope45F90 = auto()
    TestSlope45F90X = auto()
    TestSlope45F90Y = auto()
    TestSlope45F90XY = auto()

    Count = auto()

class SlopeCollisionType(Enum):
    Empty = auto()
    Block = auto()
    OneWay = auto()

    SlopeMid1 = auto()
    SlopeMid1FX = auto()
    SlopeMid1FY = auto()
    SlopeMid1FXY = auto()
    SlopeMid1F90 = auto()
    SlopeMid1F90X = auto()
    SlopeMid1F90Y = auto()
    SlopeMid1F90XY = auto()

    Slope45 = auto()
    Slope45FX = auto()
    Slope45FY = auto()
    Slope45FXY = auto()
    Slope45F90 = auto()
    Slope45F90X = auto()
    Slope45F90Y = auto()
    Slope45F90XY = auto()

    Count = auto()

class Slope:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.slopesHeights = []
        self.slopesExtended

    def get_height_maps(self):
        self.empty = [0 for x in range(16)]
        self.full = [16 for x in range(16)]
        self.slope45 = [x+1 for x in range(16)]
        self.slopeMid1 = [1,2,3,4,5,6,7,8,8,7,6,5,4,3,2,1]

        print(self.empty)

    def extend(self, Slope):


s = Slope(0, 0, 16, 16)
s.get_height_maps()
