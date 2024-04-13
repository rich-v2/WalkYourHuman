import pygame
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

class IceVendor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        human_1 = pygame.image.load('assets/ice_man/ice_man-1.png').convert_alpha()
        human_2 = pygame.image.load('assets/ice_man/ice_man-2.png').convert_alpha()

        self.stand_frames = [human_1, human_2]
        self.stand_index = 0
        self.image = self.stand_frames[self.stand_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(0, SCREEN_WIDTH),
                                                   random.randint(0, SCREEN_HEIGHT)))
        self.time = 100
        self.speed = 2
        self.dead = False
        self.scared = False
        self.in_love = False
        self.scared_timer = 0
        self.in_love_timer = 0
        self.facing = 1
        self.vertical = True

    def animation_state(self):

        self.stand_index += 0.1
        if self.stand_index > len(self.stand_frames):
            self.stand_index = 0
        self.image = self.stand_frames[int(self.stand_index)]

    def move_to_human(self, human):
        dist_x = human.sprite.rect.x - self.rect.x
        dist_y = human.sprite.rect.y - self.rect.y

        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

        if 0 < distance < 300:
            self.rect.x += self.speed * dist_x / distance
            self.rect.y += self.speed * dist_y / distance

        self.scared_timer -= 0.1
        if self.scared_timer <= 0:
            self.scared = False

    def destroy(self):
        self.time -= 0.1
        if int(self.time) == 0:
            self.kill()

    def update(self, human, win):
        if not self.dead and not self.in_love:
            self.animation_state()
            self.move_to_human(human)
        elif self.in_love:
            self.in_love_timer -= 0.1
            if self.in_love_timer <= 0:
                self.in_love = False
        else:
            self.image = pygame.image.load("assets/ice_man/ice_man-3.png")
        self.destroy()
