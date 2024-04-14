import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class Poop(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        poop_1 = pygame.image.load("assets/poop/poop-1.png").convert_alpha()
        poop_1 = pygame.transform.rotozoom(poop_1, 0, 1.5)
        self.image = poop_1.convert_alpha()
        spawn_x, spawn_y = pos
        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))
        self.timer = 100

    def slow_down(self, enemy_list):
        for enemy in pygame.sprite.spritecollide(self, enemy_list, dokill=False):
            enemy.speed = 0
            self.kill()

    def destroy(self):
        self.timer -= 0.1

        if self.timer <= 0:
            self.kill()

    def update(self, *args):
        for li in args:
            self.slow_down(li)
        self.destroy()
