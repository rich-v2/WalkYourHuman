import pygame
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class House(pygame.sprite.Sprite):

    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        house_1 = pygame.image.load("assets/house/house-1.png")
        self.image = house_1.convert_alpha()
        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))
