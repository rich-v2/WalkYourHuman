import pygame
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class Tree(pygame.sprite.Sprite):

    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        tree_1 = pygame.image.load("assets/tree/tree-1.png")
        tree_2 = pygame.image.load("assets/tree/tree-2.png")
        self.tree_frames = [tree_1, tree_2]
        self.tree_index = 0
        self.image = self.tree_frames[self.tree_index]
        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))

    def animation_state(self):
        if random.randint(0,3) > 1:
            self.tree_index += 0.05

        if self.tree_index > len(self.tree_frames):
            self.tree_index = 0

        self.image = self.tree_frames[int(self.tree_index)]

    def update(self):
        self.animation_state()
