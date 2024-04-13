import pygame
import random

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800


class Hoover(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        hoover_1 = pygame.image.load("assets/hoover/hoover-1.png")
        hoover_2 = pygame.image.load("assets/hoover/hoover-2.png")
        self.frames = [hoover_1, hoover_2]
        self.index = 0
        self.image = self.frames[self.index]
        spawn_x = SCREEN_WIDTH / 2
        spawn_y = SCREEN_HEIGHT / 2
        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))
        self.hp = 75
        self.damage_sound = pygame.mixer.Sound("music/hoover_damaged.mp3")

    def animation_state(self):
        self.index += 0.1
        if self.index > len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def move(self):
        self.rect.x += random.randint(-5, 5)
        self.rect.y += random.randint(-5, 5)

    def suck(self, player):
        dist_x = self.rect.left - player.sprite.rect.x
        dist_y = self.rect.y - player.sprite.rect.y

        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

        if 300 > distance > 50:
            player.sprite.rect.x += (player.sprite.speed-2) * dist_x / distance
            player.sprite.rect.y += (player.sprite.speed-2) * dist_y / distance

    def suck_poop(self, poop_list):
        for poop in poop_list:
            dist_x = poop.rect.x - self.rect.left
            dist_y = poop.rect.y - self.rect.center[1]

            distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

            if 300 > distance > 20:
                poop.rect.x += -2 * dist_x / distance
                poop.rect.y += -2 * dist_y / distance
            elif distance < 20:
                self.hp -= 5
                self.damage_sound.play()
                poop.kill()

    def update(self, player, poop):
        self.animation_state()
        self.move()
        self.suck(player)
        self.suck_poop(poop)
        if self.hp <= 0:
            player.sprite.win = True
            self.kill()
