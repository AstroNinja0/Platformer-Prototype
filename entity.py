import pygame

def get_collidable_objects(object, collidable_list):
    collision_list = []
    for obj in collidable_list:
        if obj.rect.colliderect(object_1):
            collision_list.append(obj)
    return collision_list

def flip(img: pygame.Surface, boolean=True):
    return pygame.transform.flip(img, boolean, False)

class Entity:
    def __init__(self, pos: list[int], size: list[int]):
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.image = pygame.Surface(size)
        self.alive = True

    @property
    def pos(self):
        return [x, y]

    @pos.setter
    def pos(self, new_pos):
        self.x, self.y = new_pos
        self.rect.x, self.rect.y = self.x, self.y
        self._pos = [self.x, self.y]

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def image(self):
        return pygame.Surface(self.size)

    @rect.setter
    def rect(self, new_rect):
        self._rect = new_rect

    @image.setter
    def image(self, new_image):
        self._image = new_image

class PhysicsEntity(Entity):
    def __init__(self, pos: list[int], size: list[int]):
        super().__init__(pos, size)
        self.gravity = 0.4
        self.movement = pygame.math.Vector2(0, 0)
        self.collision_types = {'top': False, 'bottom': False,
                                'right': False, 'left': False, 'slant_bottom': False, 'data': []}

    def x_collisions(self, tiles):
        self.rect.x += self.movement.x
        self.x = self.rect.x

        collidable_tiles = [tile for tile in get_collidable_objects(self.rect, tiles) if tile.type == 'tile']
        for tile in collidable_tiles:
            if self.movement.x > 0:
                self.rect.right = tile.rect.left
                self.collision_types['right'] = True
            elif self.movement.x < 0:
                self.rect.left = tile.rect.right
                self.collision_types['left'] = True

        if self.collision_types['left'] and self.movement.x >= 0:
            self.collision_types['left'] = False
        if self.collision_types['right'] and self.movement.x <= 0:
            self.collision_types['right'] = False

    def y_collisions(self, tiles):
        self.rect.y += self.movement.y
        self.y = self.rect.y
        self.apply_gravity()
        collidable_tiles = [tile for tile in get_collidable_objects(self.rect, tiles) if tile.type == 'tile']
        for tile in collidable_tiles:
            if self.movement.y > 0:
                self.rect.bottom = tile.rect.top
                self.collision_types['bottom'] = True
                self.movement.y = 0

            elif self.movement.y < 0:
                self.rect.top = tile.rect.bottom
                self.collision_types['top'] = True
                self.movement.y = 0

        if self.collision_types['bottom'] and self.movement.y < 0 or self.movement.y > 1:
            self.collision_types['bottom'] = False
        if self.collision_types['top'] and self.movement.y < 0.1:
            self.collision_types['top'] = False

    def ramp_collisions(self, tiles):
        ramps = [ramp for ramp in get_collidable_objects(self.rect, tiles) if tile.type == 'ramp']
        for ramp in ramps:
            if self.rect.colliderect(ramp.rect): # check if player collided with the bounding box for the ramp
                # get player's position relative to the ramp on the x axis
                rel_x = self.rect.x - ramp.rect.x
                rel_y = self.rect.y - ramp.rect.y

                # get height at player's position based on type of ramp
                if ramp.ramp == 1:
                    pos_height = rel_x + self.rect.width # go by player right edge on right ramps
                    pos_width = rel_y + self.rect.height
                elif ramp.ramp == 2:
                    pos_height = tile_size - rel_x # is already left edge by default
                    pos_width = tile_size - rel_y

                # add constraints
                pos_height = min(pos_height, tile_size)
                pos_height = max(pos_height, 0)

                pos_width = min(pos_width, tile_size)
                pos_width = max(pos_width, 0)

                target_y = ramp.rect.y + tile_size - pos_height
                target_x = ramp.rect.x + tile_size - pos_width

                if self.x < target_x and ramp.ramp == 2: # add barriers on the non-sloped edge of a ramp
                    self.rect.right = ramp.rect.left
                    collision_types['right'] = True
                elif self.x > target_x and ramp.ramp == 1:
                    self.rect.left = ramp.rect.right
                    collision_types['left'] = True

                if self.rect.bottom > target_y and not collision_types['left'] and not collision_types['right']: # check if the player collided with the actual ramp
                    # adjust player height
                    self.rect.bottom = target_y
                    self.pos[1] = self.rect.y

                    collision_types['slant_bottom'] = True
                self.x = self.rect.x

    def apply_gravity(self):
        if self.movement.y < 15:
            self.movement.y += self.gravity
        else:
            self.gravity = 0.5
            self.air_timer += 1

    def update(self, tiles):
        self.x_collisions(tiles)
        self.y_collisions(tiles)
        self.ramp_collisions(tiles)
