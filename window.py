import pygame, os
from sys import exit
from time import time

class Window:
    def __init__(self, title: str = "Super Cool Game!", size: list[int] = [640, 480], icon: pygame.Surface = None, tag = pygame.DOUBLEBUF, vsync = False, FPS = 60):
        # The base Window Stuff
        self.title = title
        self.size = size
        self.icon = icon
        self.tag = tag

        # Monitor & FPS Stuff
        self.monitor = [pygame.display.Info().current_w,
                        pygame.display.Info().current_h]
        self.vsync = vsync
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        # Deltatime stuff
        self.last_time = time()
        self.dt = 0

        # Use the sprite layer if you're using pixel art, other wise use the main display layer
        self.fullscreen = False
        self.sprite_layer = pygame.Surface([self.size[0]//2, self.size[1]//2])
        self.screen = pygame.display.set_mode(self.size, self.vsync, self.tag)
        if icon is pygame.Surface:
            pygame.display.set_icon(icon)
        pygame.display.set_caption(title)

    @property
    def size(self):
        return self._size

    # @property
    # def monitor(self):
    #     return self._monitor

    @size.setter
    def size(self, new_size: list[int]):
        self._size = new_size

    def setup_dt(self):
        self.dt = time() - self.last_time
        self.dt *= self.FPS
        self.last_time = time()
        return self.dt

    # Make a Deltatime wrapper that makes any function that moves or deals with calculations add deltatime

    def get_screen_center(self):
        temp = pygame.display.set_mode(self.monitor)
        pos_x = self.monitor[0] / 2 - self.size[0] / 2
        pos_y = self.monitor[1] / 2 - self.size[0] / 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.tag = pygame.FULLSCREEN
            self.sprite_layer = pygame.display.set_mode(self.monitor, self.tag)
            pygame.display.toggle_fullscreen()
            self.screen = pygame.display.set_mode(self.monitor, self.tag)


        else:
            self.tag = pygame.RESIZABLE
            self.sprite_layer = pygame.display.set_mode(
                self.size, self.tag)
            self.screen = pygame.display.set_mode(
                self.size, self.tag)


    def update_loop(self):
        pygame.display.update()
        self.clock.tick(self.FPS)
        self.sprite = pygame.Surface((self.size[0] // 2, self.size[1] // 2))

    def update_window(self, new_title: str, new_icon: pygame.Surface, new_size = None):
        self.title = new_title
        self.icon = new_icon
        if type(new_size) == int: self.size = new_size
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)

    def draw_sprite_layer(self):
        new_layer = pygame.transform.scale(self.sprite_layer, self.size)
        self.screen.blit(new_layer, (0,0))

    def close(self):
        pygame.quit()
        exit()
