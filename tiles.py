import pygame

class Tile():
    """Base Tile class, can be collided with all physics entities"""
    def __init__(self, size, x, y):
        self.x = x
        self.y = y
        self.size = size
        self.img = pygame.Surface((size, size))
        self.img.fill('grey')
        self.rect = pygame.Rect(x, y, size, size)

class Ramp(Tile):
    """Ramp for going up and down things"""
    def __init__(self, size, x, y, is_flipped=False):
        super().__init__(size, x, y)
        self.rect = pygame.Rect(x, y-4, size, size)
        self.flipped = is_flipped
        self.slope = (self.rect.width / self.rect.height)
        if not self.flipped:
            self.y_intercept = self.rect.topright[1]
        else:
            self.y_intercept = self.rect.topleft

class StaticRamp(Ramp):
    def __init__(self, size, x, y, surface, is_flipped = False):
        super().__init__(size, x, y, is_flipped)
        self.img = surface


class StaticTile(Tile):
    """Same as tile, but with an image :O"""
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.img = surface

class SemisolidTile(Tile):
    """Semisolid platforms that can only be collided with from the top, like Mario Maker"""
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.active = False
        self.img = surface

class Ladder(SemisolidTile):
    """Ladder tile for climbing...on ladders"""
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y, surface)
        self.climb_rect = pygame.Rect(x, y, size/2, size)

class LadderTop(SemisolidTile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y, surface)
