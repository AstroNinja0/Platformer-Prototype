import pygame
from entity import Entity
from attack import SingleAttack, Projectile, ComboLevel
from enum import Enum, auto
tile_size = 64

class PlayerState(Enum):
    Normal = auto()
    Climbing = auto()

class AstraShot(Projectile):
    def __init__(self, pos: list[int], size: list[int], speed: int, charge_lvl = 1):
        super().__init__(pos, size, speed)
        self.charge_lvl = charge_lvl

    def charge(self):
        """Charges the projectile, just like Mega Man"""
        if self.charge_lvl == 2:
            self.width, self.height = self.width * 1.5, self.height * 1.5
        elif self.charge_lvl == 3:
            self.width, self.height = self.width * 2.5, self.height * 2.5
        self.rect.width, self.rect.height = self.width, self.height
        self.image = pygame.Surface((self.width, self.height))

    def on_impact(self, tiles):
        """Is triggered when colliding with a tile or entity's hurtbox"""
        for y in tiles:
            if y:
                for tile in y:
                    if self.rect.colliderect(tile.rect):
                        self.alive = False

def collision_test(object_1, object_list):
    collision_list = []
    for y in object_list:
        if y:
            for obj in y:
                if obj.rect.colliderect(object_1):
                    collision_list.append(obj)
    return collision_list

def get_collisions(entity, tiles):
    x = entity.x // tile_size
    y = entity.y // tile_size
    print(x, y)
    collision_list = []
    try:
        if entity.rect.colliderect(tiles[y][x].rect):
            collision_list.append(tiles[y][x])
    except IndexError:
        print("Tile does not exist!")
    return collision_list

class Player:
    """The player, soon to be Astra-chan"""
    def __init__(self, x: int, y: int, x_size: int, y_size: int):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size

        # Player Movement
        self.movement = pygame.math.Vector2(0, 0)
        self.wall_jump_movement = pygame.math.Vector2(0, 0)
        self.momentum = pygame.math.Vector2(0, 0)
        self.gravity = 0.4

        # Timers and caps
        self.air_timer = 0
        self.jump_timer = 0
        self.dash_timer = 0
        self.wall_jump_timer = 0
        self.charge_timer = 0
        self.sabre_timer = 0
        self.sabre_attack_counter = 0

        self.air_timer_cap = 6
        self.jump_cancel_cap = 20
        self.dash_timer_cap = 15
        self.wall_jump_cap = 12
        self.attacks = []


        self.move_speed = 6
        self.jump_height = 0
        self.jump_height_max = -12
        self.wall_jump_speed = 10

        # Attack Stuff
        self.projectiles = []
        self.main_charge = 1
        self.sub_charge = 1


        self.img = pygame.Surface((x_size, y_size))
        # TEMP DEBUG STUFF
        self.img.fill('red')
        self.rect = self.img.get_rect(topleft=(x, y))

        self.collision_types = {'top': False, 'bottom': False,
                                'right': False, 'left': False, 'slant_bottom': False, 'data': []}
        self.flipped = False
        self.player_state = PlayerState.Normal
        self.normal_actions = {'move_left': False, 'move_right': False, 'on_wall': False, 'jumping': False,
                       'wall_jumping': False, 'dashing': False, 'on_ground': False, 'melee_attack': False, 'shooting': False, 'enter_climb':False}
        self.climbing_actions = {'climb_up': False, 'climb_down': False, 'ladder_jump': False}

    def get_input(self, key, display):  # Use in Game Loop
        match self.player_state:
            case PlayerState.Normal:
                if key.type == pygame.KEYDOWN:

                    if key.key == pygame.K_UP:
                        self.normal_actions['enter_climb'] = True

                    if key.key == pygame.K_RIGHT:
                        self.normal_actions['move_right'] = True

                    if key.key == pygame.K_LEFT:
                        self.normal_actions['move_left'] = True

                    if (key.key == pygame.K_SPACE):# or key.key == pygame.K_UP):
                        self.normal_actions['jumping'] = True

                    if key.key == pygame.K_z:
                        self.normal_actions['dashing'] = True

                    if key.key == pygame.K_w:
                        for i in range(1, 20):
                            self.rect.x += 5

                    if key.key == pygame.K_x:
                        self.normal_actions['shooting'] = True
                        self.shoot()

                    # melee_attack
                    if key.key == pygame.K_c:
                        self.melee(display)


                if key.type == pygame.KEYUP:
                    if key.key == pygame.K_RIGHT:
                        self.normal_actions['move_right'] = False

                    if key.key == pygame.K_LEFT:
                        self.normal_actions['move_left'] = False

                    if (key.key == pygame.K_SPACE):# or key.key == pygame.K_UP):
                        self.normal_actions['jumping'] = False

                    # Make it so the dash
                    if key.key == pygame.K_z and self.air_timer == 0:
                        self.normal_actions['dashing'] = False

                    if key.key == pygame.K_x:
                        if self.charge_timer >= 30:
                            self.shoot()
                        self.main_charge = 1
                        self.normal_actions['shooting'] = False

                    if key.key == pygame.K_UP:
                        self.normal_actions['enter_climb'] = False

            case PlayerState.Climbing:
                if key.type == pygame.KEYDOWN:
                    if key.key == pygame.K_UP:
                        self.climbing_actions['climb_up'] = True
                        # Climb up
                    if key.key == pygame.K_DOWN:
                        self.climbing_actions['climb_down'] = True
                        #Climb Down
                    if key.key == pygame.K_SPACE:
                        self.climbing_actions['ladder_jump'] = True

                if key.type == pygame.KEYUP:
                    if key.key == pygame.K_UP:
                        self.climbing_actions['climb_up'] = False
                        # Climb up

                    if key.key == pygame.K_DOWN:
                        self.climbing_actions['climb_down'] = False

                    if key.key == pygame.K_SPACE:
                        self.climbing_actions['ladder_jump'] = False

    def x_movement(self, tiles):
        # Wall jump code
        if self.normal_actions['wall_jumping'] and self.normal_actions['jumping']:
            self.rect.x += self.wall_jump_movement.x * 20

            if self.normal_actions['dashing']:
                self.dash()
                self.rect.x += self.wall_jump_movement.x * 40

        else:
            self.rect.x += self.movement.x
        self.x = self.rect.x
        hit_list = collision_test(self, tiles)
        for tile in hit_list:
            if self.movement.x > 0:
                self.rect.right = tile.rect.left
                self.collision_types['right'] = True
                self.wall_slide()

            if self.movement.x < 0:
                self.rect.left = tile.rect.right
                self.collision_types['left'] = True
                self.wall_slide()

        if self.collision_types['left'] and self.movement.x >= 0:
            self.collision_types['left'] = False
        if self.collision_types['right'] and self.movement.x <= 0:
            self.collision_types['right'] = False

    def y_movement(self, tiles):
        if self.normal_actions['wall_jumping'] and self.normal_actions['jumping']:
            self.rect.y += self.wall_jump_movement.y * 10
        else:
            self.rect.y += self.movement.y
        self.y = self.rect.y
        hit_list = collision_test(self, tiles)
        if self.player_state == PlayerState.Normal:
            self.apply_gravity()

        for tile in hit_list:
            if self.movement.y > 0:
                self.rect.bottom = tile.rect.top
                self.collision_types['bottom'] = True
                self.movement.y = 0

            elif self.movement.y < 0:
                self.rect.top = tile.rect.bottom
                self.collision_types['top'] = True
                self.movement.y = 0
                self.jump_timer = 21

        if self.collision_types['bottom'] and self.movement.y < 0 or self.movement.y > 1:
            self.collision_types['bottom'] = False
        if self.collision_types['top'] and self.movement.y < 0.1:
            self.collision_types['top'] = False

    def ramp_movement(self, ramps):
        """Ramps are fun...right?"""
        Ramps = collision_test(self, ramps)
        for ramp in Ramps:
            if self.rect.colliderect(ramp.rect):
                rel_x = self.rect.x - ramp.rect.x

                pos_height = rel_x + self.rect.width

                pos_height = min(pos_height, ramp.rect.height)
                pos_height = max(pos_height, 0)

                if ramp.flipped:
                    target_y = ramp.rect.y + pos_height * (ramp.rect.height / ramp.rect.width)
                else:
                    target_y = ramp.rect.y - (pos_height - ramp.rect.height)


                if self.rect.bottom > target_y:
                    self.rect.bottom = target_y
                    self.collision_types['bottom'] = True
                    self.movement.y = 0


    def semisolid_movement(self, semisolids):
        Semisolids = collision_test(self, semisolids)
        for semisolid in Semisolids:
            if self.rect.y+self.rect.height/2 < semisolid.rect.top-1 :
            #     semisolid.active = True
            # else:
            #     semisolid.active = False

                if self.rect.colliderect(semisolid.rect):
                    if self.movement.y > 0:
                        self.rect.bottom = semisolid.rect.top
                        self.movement.y = 0
                        self.collision_types['bottom'] = True

    def ladder_movement(self, ladders):
        Ladders = collision_test(self, ladders)
        print(Ladders)
        for ladder in Ladders:
            if self.rect.colliderect(ladder.rect) and self.normal_actions['enter_climb']:
                self.player_state = PlayerState.Climbing
                self.climb(ladder)
        if not Ladders:
            self.player_state = PlayerState.Normal

    def climb(self, ladder):
        acceleration = 1.5
        climb_cap = 3
        self.rect.x = ladder.climb_rect.centerx
        self.x = self.rect.x
        self.movement.x = 0
        # Lock the player's X axis to the ladder's climb rect & make the y axis able to traverse the Y axis
        if self.climbing_actions['climb_up']:
            self.movement.y -= acceleration
        elif self.climbing_actions['climb_down']:
            self.movement.y += acceleration
        else:
            self.movement.y = 0

        if abs(self.movement.y) > climb_cap:
            if self.climbing_actions['climb_up']:
                self.movement.y = -climb_cap
            else:
                self.movement.y = climb_cap

        # Jumping from Ladder:
        if self.climbing_actions['ladder_jump']:
            self.normal_actions['enter_climb'] = False
            self.player_state = PlayerState.Normal
            self.climbing_actions['ladder_jump'] = False

    def input_actions(self):
        acceleration = 1.5

        if self.normal_actions['move_right']:
            if self.normal_actions['move_left'] and self.movement.x < 0:
                self.movement.x = 0
            self.movement.x += acceleration
            self.flipped = False
        elif self.normal_actions['move_left']:
            if self.normal_actions['move_right'] and self.movement.x > 0:
                self.movement.x = 0
            self.movement.x -= acceleration
            self.flipped = True
        else:
            self.movement.x = 0

        if abs(self.movement.x) > self.move_speed or self.normal_actions['dashing']:
            if self.normal_actions['move_left']:
                self.movement.x = -self.move_speed
            if self.normal_actions['move_right']:
                self.movement.x = self.move_speed


        if self.normal_actions['jumping']:
            if self.air_timer < 6:
                self.jump()
            self.jump_timer += 1

        # Makes it so the player, when jumping is false, can cancel the height
        if self.jump_timer <= self.jump_cancel_cap and self.normal_actions['jumping'] == False and not self.collision_types['bottom']:
            self.movement.y = 0
            self.jump_timer = 21

        # Dash
        if self.normal_actions['dashing'] and self.air_timer < 1:
            if self.dash_timer < self.dash_timer_cap:
                self.dash()
                if not (self.normal_actions['move_right'] or self.normal_actions['move_left']):
                    if self.flipped:
                        self.movement.x = -self.move_speed
                    else:
                        self.movement.x = self.move_speed
            else:
                self.normal_actions['dashing'] = False
                self.dash_timer = self.dash_timer_cap
        if self.normal_actions['dashing'] == False:
            self.dash_timer = 0
            self.move_speed = 6

        # Make it so when the player hits the ground after jumping,
        # the dash stops
        if self.air_timer >= self.air_timer_cap and self.collision_types['bottom']:
            self.normal_actions['dashing'] = False

        # Wall Jump
        if self.normal_actions['jumping'] and self.normal_actions['on_wall']:
            self.normal_actions['wall_jumping'] = True
        if self.normal_actions['wall_jumping']:
            if self.wall_jump_timer < self.wall_jump_cap:
                self.wall_jump()

                self.wall_jump_timer += 1
            else:
                self.normal_actions['wall_jumping'] = False
                self.normal_actions['on_wall'] = False
                self.wall_jump_timer = 0
        # if self.wall_jump_timer > 0 and self.normal_actions['on_wall'] and self.normal_actions['dashing']:
            # self.normal_actions['dashing'] = False

        # Charge Shot
        if self.normal_actions['shooting']:
            # Sets the charge levels
            if self.charge_timer == 0:
                self.main_charge = 1
            elif self.charge_timer == 30:
                self.main_charge = 2
            elif self.charge_timer == 70:
                self.main_charge = 3

            if self.charge_timer < 70:
                self.charge_timer += 1
            else:
                self.charge_timer = 70
        else:
            self.charge_timer = 0

    def dash(self):
        self.dash_direction = pygame.math.Vector2(1,0).normalize().x * 10
        self.move_speed = self.dash_direction
        if self.collision_types['bottom']:
            self.dash_timer += 0.7

    def apply_gravity(self):
        if self.movement.y < 15:
            self.movement.y += self.gravity
        if self.collision_types['bottom'] or self.collision_types['slant_bottom']:
            self.air_timer = 0
            self.jump_timer = 0
            self.wall_jump_timer = 0
            self.normal_actions['on_wall'] = False
        else:
            self.gravity = 0.5
            self.air_timer += 1

    def jump(self):
        self.movement.y = self.jump_height_max

    def wall_jump(self):
        # We want to disable the player movement while the wall jump
        # movement is occuring'
        # Maybe get a directional vector and send the player in that direction for a period of time

        if self.collision_types['right']:
            self.wall_jump_movement = pygame.math.Vector2(-1, -5).normalize()
        elif self.collision_types['left']:
            self.wall_jump_movement = pygame.math.Vector2(1, -5).normalize()
        if self.normal_actions['jumping']:
            self.movement.y = -6
        else:
            self.movement.y = 0

    def wall_slide(self):
        if self.collision_types['bottom'] == False and self.movement.y > -2:
            # self.movement.x = 0
            self.normal_actions['on_wall'] = True
            if self.movement.y < 4:
                self.movement.y += 0.5
            else:
                self.movement.y = 4

    def shoot(self):
        # If the length of the projectile list is less than 4
        # Create a projectile & add it to the list
        # If a projectile is destroyed, remove it from the list
        if len(self.projectiles) < 4:
            if self.flipped:
                if self.main_charge == 1:
                    astra_shot = AstraShot([self.x-self.rect.width, self.rect.y], [9, 9], 15)
                elif self.main_charge == 2:
                    astra_shot = AstraShot([self.x-self.rect.width, self.rect.y], [9, 9], 15, 2)
                else:
                    astra_shot = AstraShot([self.x-self.rect.width, self.rect.y+self.rect.height], [9, 9], 15, 3)
                astra_shot.charge()
                astra_shot.trajectory = pygame.math.Vector2(-1,0).normalize()
            else:
                if self.main_charge == 1:
                    astra_shot = AstraShot([self.x+self.rect.width, self.rect.y], [9, 9], 15)
                elif self.main_charge == 2:
                    astra_shot = AstraShot([self.x+self.rect.width, self.rect.y], [9, 9], 15, 2)
                else:
                    astra_shot = AstraShot([self.x+self.rect.width, self.rect.y+self.rect.height], [9, 9], 15, 3)
                astra_shot.charge()
                astra_shot.trajectory = pygame.math.Vector2(1,0).normalize()
            self.projectiles.append(astra_shot)

    def melee(self, display):
        # Spawn a rect that's red for now, if the button is pressed while standing still, allow for a three hit combo
        # If the player is moving, jumping, or on a wall, allow for only one attack
        attack = AstraSabre(self, 5, [10, 15], 15, ComboLevel.lvl_1, [self.rect.width, self.rect.height])
        self.attacks.append(attack)

    def update(self, collision_tiles, collision_ramps, collision_semisolids, collision_ladders):
        self.input_actions()
        self.x_movement(collision_tiles)
        self.y_movement(collision_tiles)
        self.ramp_movement(collision_ramps)
        self.semisolid_movement(collision_semisolids)
        self.ladder_movement(collision_ladders)
        for _, shot in sorted(enumerate(self.projectiles), reverse = True):
            shot.update()
            shot.on_impact(collision_tiles+collision_ramps)

            # Modifies the list mid-iteration
            self.projectiles[:] = [p for p in self.projectiles if p.alive]

        for _, attack in sorted(enumerate(self.attacks), reverse = True):
            # Modifies the list mid-iteration
            self.attacks[:] = [a for a in self.attacks if attack.active]

class AstraSabre(SingleAttack):
    def __init__(self, player: Player, duration: int, size: list[int], damage: int, combo_lvl = ComboLevel, offset = [0, 0]):
        super().__init__(player, duration, size, damage, combo_lvl, offset)
        self.x = player.x + player.rect.width
        self.y = player.y
        self.countdown()
