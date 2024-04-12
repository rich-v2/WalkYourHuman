import pygame
import random
from projectile import Projectile


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800


class BurgerFlinger(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        flinger_1 = pygame.image.load("assets/burger_flinger/burgerFlinger-1.png")
        flinger_2 = pygame.image.load("assets/burger_flinger/burgerFlinger-2.png")
        self.frames = [flinger_1, flinger_2]
        self.index = 0
        self.image = self.frames[self.index]
        spawn_x = random.randint(100, SCREEN_WIDTH - 100)
        spawn_y = random.randint(100, SCREEN_HEIGHT - 100)
        self.rect = self.image.get_rect(midbottom=(spawn_x, spawn_y))
        self.dead = False
        self.left = False
        self.timer = 135
        self.fling_timer = 0
        self.patties = []
        self.fling_sound = pygame.mixer.Sound("music/fling_sound.mp3")
        self.scared = False
        self.speed = 2

    def move_to_human(self, human):
        human_x, human_y = human.sprite.rect.center
        flinger_x, flinger_y = self.rect.center
        if flinger_x < human_x:
            self.left = False
        else:
            self.left = True
        if flinger_y < human_y:
            new_y = flinger_y + 1
        elif flinger_y > human_y:
            new_y = flinger_y - 1
        else:
            new_y = flinger_y
        if human_x - 200 < flinger_x < human_x:
            new_x = flinger_x - 1
        elif human_x < flinger_x < human_x + 200:
            new_x = flinger_x + 1
        else:
            new_x = flinger_x
        self.rect.center = (new_x, new_y)

    def animation_state(self):
        self.index += 0.1
        if self.index > len(self.frames):
            self.index = 0

        self.image = self.frames[int(self.index)]

    def fling(self, win):
        if len(self.patties) < 3 and self.fling_timer <= 0:
            spawn_x, spawn_y = self.rect.center
            if self.left:
                face = -1
            else:
                face = 1
            self.patties.append(Projectile(spawn_x, spawn_y, 4,
                                           "brown", face))
            self.fling_sound.play()
            self.fling_timer = 10
        else:
            self.fling_timer -= 0.1

        for patty in self.patties:
            if SCREEN_WIDTH > patty.x > 0:
                patty.x += patty.vel
                patty.draw(win)
            else:
                self.patties.pop(self.patties.index(patty))

    def destroy(self):
        self.timer -= 0.1
        if self.timer <= 0:
            self.kill()

    def update(self, human, win):
        if not self.dead:
            self.animation_state()
            self.move_to_human(human)
            self.fling(win)
        else:
            self.image = pygame.image.load("assets/burger_flinger/burgerFlinger-3.png")
        self.destroy()


