import pygame
from window import Window
from player import Player
from camera import *
from level import Level
pygame.init()

screen = Window("Platformer Shenanigans", [1920, 1080])


level = Level("src/config/level_test.json")
player = Player(2000,430, 30, 32)
camera = Camera(screen.screen,complex_camera)
fg_entities = [player]
fg_tiles = [level.terrain_types]

background_rects = [pygame.Rect(20,-300,70,400), pygame.Rect(280, 30, 40, 400), pygame.Rect(30,40,40,400), pygame.Rect(300,80,120,400)]

overlay = pygame.Surface((1280, 720))
overlay_rect = pygame.Rect(0, 0, 1280, 720)

def main():
    while True:
        screen.screen.fill((0,0,40))
        
        for event in pygame.event.get():
            player.get_input(event, screen.screen)
            if event.type == pygame.QUIT:
                screen.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen.close()
                if event.key == pygame.K_f:
                    screen.toggle_fullscreen()
                if event.key == pygame.K_p:
                    pass
        # Rendering Temp Stuff
        # for rect in background_rects:
        #     pygame.draw.rect(screen.screen, 'blue', camera.apply_bg_rect(rect))



        for shot in player.projectiles:
            if shot.rect.x not in range(player.x - (WINDOW[0]//2), player.x + (WINDOW[0]//
            2)):
                shot.alive = False
            if shot.charge_lvl == 1:
                pygame.draw.circle(screen.screen, (220, 20, 60), [camera.apply(shot)[0], camera.apply(shot)[1]], shot.height-2)
            elif shot.charge_lvl == 2:
                pygame.draw.circle(screen.screen, 'green', [camera.apply(shot)[0], camera.apply(shot)[1]], shot.height-2)
            else:
                pygame.draw.circle(screen.screen, 'purple', [camera.apply(shot)[0], camera.apply(shot)[1]], shot.height-2)

        for attack in player.attacks:
            pygame.draw.rect(screen.screen, 'pink', camera.apply_rect(attack.hitbox))

        camera.draw_sprites(fg_entities)
        camera.draw_tiles(level.terrain_types)
        camera.update(player)

        player.update(level.terrain_types['terrain'], level.terrain_types['ramps'], level.terrain_types['semisolids'], level.terrain_types['ladders'])
        screen.update_loop()


if __name__ == '__main__':
    main()
