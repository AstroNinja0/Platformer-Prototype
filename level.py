import pygame
from csv import reader
from json import load
from numpy import multiply
from tiles import StaticTile, StaticRamp, SemisolidTile, Ladder, LadderTop
tile_size = 64

def read_layout(path: str) -> list:
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ",")
        for y in level:
            terrain_map.append(list(y))
        return terrain_map

def import_cut_graphics(path: str) -> list[pygame.Surface]:
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] // tile_size)
    tile_num_y = int(surface.get_size()[1] // tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = multiply(col, tile_size)
            y = multiply(row, tile_size)
            new_surf = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
    return cut_tiles

def open_json(path: str) -> dict:
    with open(path) as f:
        data = load(f)
        return data

class Level():
    def __init__(self, level_data: str):
        """Needs a JSON with the level data in order to function!"""
        # Base setup
        self.level_data = level_data # Gets the path from a JSON with all of the data stuff inside

        self.info = {}
        self.tile_layouts = {}

        self.terrain_types = {}
        self.background_assets = {}

        self.tile_images = {}
        self.tile_groups = {}
        self.read_level_data()
        self.setup_level()

    def read_level_data(self):
        """Reads in the level data from a JSON file"""
        lvl_data = open_json(self.level_data)
        for stuff in lvl_data:
            if stuff == 'world_info':
                self.info = lvl_data[stuff]
            elif stuff == 'tile_layouts':
                self.tile_layouts = lvl_data[stuff]
            elif stuff == 'tile_images':
                self.tile_images = lvl_data[stuff]

    def setup_level(self):
        """Sets up the level from the JSON data"""
        for layout in self.tile_layouts:
            for layer1, type in self.tile_layouts[layout].items():
                if type != "None":
                    if layer1 == 'fg_tiles':
                        for layer2, data in self.tile_layouts[layout][layer1].items():
                            if data != "None":
                                self.terrain_types[layer2] = self.load_layout(layer2, data, self.tile_images[layout][layer1][layer2])
                    elif layer1 == 'bg_tiles_1':
                        for layer2, data in self.tile_layouts[layout][layer1].items():
                            if data != "None":
                                self.background_assets[layer2] = self.load_layout(layer2, data, self.tile_images[layout][layer1][layer2])

                    # self.tile_groups[layer] = self.terrain_types[layer2]

    def load_layout(self, type, layout_path: str, img_path):
        tile_layout = read_layout(layout_path)
        sprites = self.load_tile_group(tile_layout, img_path, type)
        return sprites

    def load_tile_group(self, layout: list[int], img: str, type: str):
        """Loads tile groups for the level"""
        sprite_group = []

        for row_index, row in enumerate(layout):
            x_list = []
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    terrain_tile_list = import_cut_graphics(img)
                    tile_surface = terrain_tile_list[int(val)]

                    if type == 'terrain':
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'ramps':
                        sprite = StaticRamp(tile_size, x, y, tile_surface)

                    if type == 'semisolids':
                        sprite = SemisolidTile(tile_size, x, y, tile_surface)

                    if type == 'ladders':
                        sprite = Ladder(tile_size, x, y, tile_surface)

                    x_list.append(sprite)
            sprite_group.append(x_list)
        return sprite_group

if __name__ == '__main__':
    screen = pygame.display.set_mode((400, 300))
    level = Level("src/config/level_test.json")
