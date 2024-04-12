import pygame
import random
from burger_flinger import BurgerFlinger


class Dog(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.frames = []
        self.index = 0
        self.image = None
        self.rect = None
        self.speed = 5
        self.closest_enemy = None
        self.timer = 135

    def move_to_flinger(self, enemy_list):
        distance = 10000
        dist_x_closest = 0
        dist_y_closest = 0
        for enemy in enemy_list:
            if isinstance(enemy, BurgerFlinger):
                dist_x = enemy.rect.centerx - self.rect.centerx
                dist_y = enemy.rect.centery - self.rect.centery
                distance_enemy = (dist_x ** 2 + dist_y ** 2) ** 0.5
                if distance_enemy < distance:
                    distance = distance_enemy
                    dist_x_closest = dist_x
                    dist_y_closest = dist_y
                    self.closest_enemy = enemy
        if distance > 10:
            self.rect.centerx += self.speed * dist_x_closest / distance
            self.rect.centery += self.speed * dist_y_closest / distance

    def animation_state(self):
        self.index += 0.1
        if self.index > len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def destroy(self):
        self.timer -= 0.1
        if self.timer <= 0:
            self.kill()

    def update(self, enemy_list):
        self.animation_state()
        self.move_to_flinger(enemy_list)
        self.destroy()


class Pug(Dog):

    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        frame_1 = pygame.image.load("assets/pug/pug-1.png")
        frame_2 = pygame.image.load("assets/pug/pug-2.png")
        self.frames = [frame_1, frame_2]
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))





