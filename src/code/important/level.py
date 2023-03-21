import pygame
from csv import reader
from numpy import divide, multiply
from tiles import StaticTile
tile_size = 64

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ",")
        for y in level:
            terrain_map.append(list(y))
        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] // tile_size)
    tile_num_y = int(surface.get_size()[1] // tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

class Level():
    def __init__(self, surface: pygame.Surface):
        # Base setup
        self.display = surface
        self.sprite_list = []

        self.terrain_layout = import_csv_layout("src/level_data/csv_layout/test_map_terrain.csv")
        self.terrain_sprites = self.load_tile_group(self.terrain_layout,'terrain')
        self.bg_sprites1 = None
        self.bg_sprites2 = None

        # self.bg_scroll1 = list(map(lambda x: int(divide(x, 2)), scroll))
        # self.bg_scroll2 = list(map(lambda x: int(divide(x, 2)), scroll))

    def load_layout(self, layout_path, img_path):
        layout = import_csv_layout(layout_path)
        sprites = self.load_tile_group(layout, 'terrain')

    def load_tile_group(self, layout, type):
        sprite_group = []

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(
                            'src/img/static/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    sprite_group.append(sprite)
        return sprite_group

    # def render_tiles(self, scroll):
    #     for sprite in self.foreground_sprites:
    #         self.display.blit(sprite.img, (sprite.x-scroll[0], sprite.y-scroll[1]))
