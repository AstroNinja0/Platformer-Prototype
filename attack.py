import pygame
from entity import Entity
from enum import Enum, auto

class ComboLevel(Enum):
    """Combo level for combos the player can perform, enemies can't combo"""
    lvl_1 = auto()
    lvl_2 = auto()
    lvl_3 = auto()
    lvl_4 = auto()

class Attack:
    """Main class thingy for all attacks"""
    def __init__(self, entity: Entity, duration: int, size: list[int], damage: int, combo_lvl = ComboLevel, offset = [0, 0]):
        self.entity = entity
        self.duration = duration # How long the attack should last
        self.damage = damage
        self.size = size
        self.offset = offset
        self.active = True

class Projectile(Entity):
    def __init__(self, pos: list[int], size: list[int], trajectory: pygame.Vector2, speed: int = 1):
        super().__init__(pos, size)
        self.speed = speed
        self.trajectory = pygame.math.Vector2(1, 0).normalize()

    def update(self):
        self.x += self.trajectory.x * self.speed
        self.y += self.trajectory.y * self.speed

        self.rect.x, self.rect.y = self.x, self.y

class SingleAttack(Attack):
    """Single attacks only have one hitbox that deals one consistent damage chunk"""
    def __init__(self, entity: Entity, duration: int, size: list[int], damage: int, combo_lvl = ComboLevel, offset = [0, 0]):
        super().__init__(entity, duration, size, damage, combo_lvl, offset)
        self.hitbox = pygame.Rect(
        entity.x + offset[0], entity.y + offset[1], size[0], size[1])
        self.timer = 0

    def countdown(self):
        """Simple countdown so the hitbox lasts for the duration of the attack"""
        print("PEE")
        while self.timer < self.duration:
            self.update()
            self.timer += 1
        else:
            self.active = False

    def update(self):
        """Updates the attack so that it sticks to the player"""
        print(self.hitbox.x)
        self.hitbox.x = self.entity.x + self.offset[0]
        self.hitbox.y = self.entity.y - self.offset[1]
        # self.countdown()

class MultiAttack(Attack): # We'll get to you later ;)
    """Multi-Attacks deal multiple hits of damage in a sequential order"""
    def __init__(self, entity: Entity, duration: int, size: list[int], damage: int, combo_lvl = ComboLevel, offset = [0, 0]):
        super().__init__(entity, duration, size, damage, combo_lvl, offset)
