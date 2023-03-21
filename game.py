import pygame
from window import Window
from player import Player
from camera import *
from level import Level

# For easier running of da game, come back to this at some point but for now imma leave it as is
class Game():
    def __init__(self):
        self.window = Window("Platformer Shenanigans", [1280, 720])
        self.player = Player(2500,430, 20, 20)
        self.level = Level(self.window.screen)
        self.camera = Camera(self.window.screen, complex_camera, len(level.terrain_layout[0])*64, len(level.terrain_layout)*64)

    def run(self):
        while True:
            self.window.screen.fill((0,0,40))

            for event in pygame.event.get():
                player.get_input(event)
                if event.type == pygame.QUIT:
                    screen.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen.close()
                    if event.key == pygame.K_f:
                        screen.toggle_fullscrxeen()
                    if event.key == pygame.K_p:
                        pass

            for rect in background_rects:
                pygame.draw.rect(self.window.screen, 'blue', self.camera.apply_bg_rect(rect))

            for shot in player.projectiles:
                pygame.draw.circle(self.window.screen, 'blue', [self.camera.apply(shot)[0], self.camera.apply(shot)[1]], shot.width)


            self.camera.draw_sprites(fg_entities)

            # The Projectiles when summoned doesn't get destroyed when going off-screen
            self.camera.update(player)
            self.player.update(self.window.screen, self.level.terrain_sprites, self.camera)

            self.window.update_loop()
