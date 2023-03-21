import pygame

class Tile():
    def __init__(self, size, x, y, type = 'tile'):
        self.x = x
        self.y = y
        self.size = size
        self.img = pygame.Surface((size, size))
        self.img.fill('grey')
        self.rect = pygame.Rect(x, y, size, size)
        self.type = type

        if self.type == 'ramp':
            self.flipped = False

class StaticTile(Tile):
    def __init__(self, size, x, y, surface, type = 'tile'):
        super().__init__(size, x, y, type)
        self.img = surface

ramp = Tile(64, 0, 0, 'ramp')
print(ramp.flipped)
