import pygame
from numpy import divide
WINDOW = [1280, 720]
true_scroll = [0,0]

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect # l = left,  t = top
    _, _, w, h = camera      # w = width, h = height
    return pygame.Rect(-l+WIN_WIDTH/2, -t+WIN_HEIGHT/2, w, h)

def complex_camera(camera, target_rect, add_border=False):
    # we want to center target_rect
    x = -target_rect.center[0] + WINDOW[0]/2
    y = -target_rect.center[1] + WINDOW[1]/2+40
    # move the camera. Let's use some vectors so we can easily substract/multiply
    camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft)) / 15 # add some smoothness coolnes
    # set max/min x/y so we don't see stuff outside the world
    if add_border:
        camera.x = max(-(camera.width-WINDOW[0]), min(0, camera.x))
        camera.y = max(-(camera.height-WINDOW[1]), min(0, camera.y))

    return camera

def setup_scroll(target): # Used for parallax
    true_scroll[0] += (target.x - true_scroll[0] - (WINDOW[0]/2 + target.rect.width/2)) / 20
    true_scroll[1] += (target.y - true_scroll[1] - (WINDOW[0]/2 + target.rect.height/2) + target.rect.height/2) / 20
    scroll = list(map(int, true_scroll))
    return scroll

class Camera(object):
    def __init__(self, display, camera_func, width, height):
        self.display = display
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def apply_rect(self, target_rect):
        return target_rect.move(self.state.topleft)

    def apply_bg1(self, target):
        return target.rect.move(self.state.topleft[0]/2, self.state.topleft[1]/2)

    def apply_bg2(self, target):
        return target.rect.move(self.state.topleft[0]/4, self.state.topleft[1]/4)

    def apply_bg_rect(self, target):
        return target.move(self.state.topleft[0]/2, self.state.topleft[1]/2)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def draw_sprites(self, fg_entities, bg1_entities=[], bg2_entities=[]):
        mode = None
        for entity in fg_entities+bg1_entities+bg2_entities:
            if entity in fg_entities:
                mode = self.apply(entity)
            elif entity in bg2_entities:
                mode = self.apply_bg(entity)
            else:
                mode = self.apply_bg2(entity)
            self.display.blit(entity.img, mode)
