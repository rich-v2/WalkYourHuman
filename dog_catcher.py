import pygame
import random
from ice_vendor import IceVendor

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class DogCatcher(IceVendor):

    def __init__(self, player):
        super().__init__(player)
        catcher_1 = pygame.image.load("assets/dog_catcher/dog_catcher-1.png")
        catcher_2 = pygame.image.load("assets/dog_catcher/dog_catcher-2.png")

        self.stand_frames = [catcher_1, catcher_2]
        self.stand_index = 0
        self.image = self.stand_frames[self.stand_index]
        spawn_x = random.randint(0, SCREEN_WIDTH)
        spawn_y = random.randint(0, SCREEN_HEIGHT)
        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))
        self.catch_timer = 10
        self.speed = 4

    def update(self, human):
        if not self.dead:
            self.animation_state()
            self.move_to_human(human)
            self.destroy()
        else:
            self.image = pygame.image.load("assets/dog_catcher/dog_catcher-3.png")
            self.catch_timer -= 0.1
            if self.catch_timer <= 0:
                self.kill()



