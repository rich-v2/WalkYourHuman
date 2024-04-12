import pygame
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class Apple(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        apple_1 = pygame.image.load("assets/apple/apple-1.png")
        apple_2 = pygame.image.load("assets/apple/apple-2.png")

        self.frames = [apple_1, apple_2]
        self.index = 0

        self.image = self.frames[self.index]
        spawn_x = random.randint(10, SCREEN_WIDTH - 10)
        spawn_y = random.randint(10, SCREEN_HEIGHT - 10)
        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))

        self.timer = 100

    def animation_state(self):
        self.index += 0.1
        if self.index > len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.animation_state()
        self.timer -= 0.1
        if self.timer <= 0:
            self.kill()