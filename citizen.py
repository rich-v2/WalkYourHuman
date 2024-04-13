import pygame
import random

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800


class Citizen(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        frame_1 = pygame.image.load("assets/lady/princess-1.png").convert_alpha()
        frame_2 = pygame.image.load("assets/lady/princess-2.png").convert_alpha()

        self.frames = [frame_1, frame_2]
        self.index = 0

        self.image = self.frames[self.index]
        self.spawn_x = random.randint(50, SCREEN_WIDTH - 50)
        self.spawn_y = random.randint(50, SCREEN_HEIGHT - 50)
        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))
        self.timer = 200
        self.width = random.randint(self.spawn_x, SCREEN_WIDTH - 50)
        self.height = random.randint(self.spawn_y, SCREEN_HEIGHT - 50)
        self.scared = False
        self.direction = 6
        self.move_dir = random.choice([1, 2, 3, 4])
        self.in_love = False

    def animation_state(self):
        self.index += 0.1
        if self.index > len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def move(self):
        if self.move_dir == 1:
            if self.rect.centerx < self.spawn_x + self.width and self.rect.centery < self.spawn_y + self.height:
                self.rect.centerx += 1
            elif self.rect.centery < self.spawn_y + self.height:
                self.rect.centery += 1
            elif self.rect.centerx > self.spawn_x:
                self.rect.centerx -= 1
            elif self.rect.centerx == self.spawn_x and self.rect.centery > self.spawn_y:
                self.rect.centery -= 1
        elif self.move_dir == 2:
            if self.rect.centerx > self.spawn_x - self.width and self.rect.centery < self.spawn_y + self.height:
                self.rect.centerx -= 1
            elif self.rect.centery < self.spawn_y + self.height:
                self.rect.centery += 1
            elif self.rect.centerx < self.spawn_x + self.width:
                self.rect.centerx += 1
            elif self.rect.centerx == self.spawn_x + self.width and self.rect.centery < self.spawn_y + self.height:
                self.rect.centery -= 1
        elif self.move_dir == 3:
            if self.rect.centery < self.spawn_y + self.height and self.rect.centerx < self.spawn_x + self.width:
                self.rect.centery += 1
            elif self.rect.centerx < self.spawn_x + self.width:
                self.rect.centerx += 1
            elif self.rect.centerx == self.spawn_x + self.width and self.rect.centery < self.spawn_y:
                self.rect.centery -= 1
            elif self.rect.centerx > self.spawn_x:
                self.rect.centerx -= 1
        elif self.move_dir == 4:
            if self.rect.centery > self.spawn_y - self.height and self.rect.centerx == self.spawn_x:
                self.rect.centery -= 1
            elif self.rect.centerx < self.spawn_x + self.width:
                self.rect.centerx += 1
            elif self.rect.centery < self.spawn_y:
                self.rect.centery += 1
            elif self.rect.centerx > self.spawn_x:
                self.rect.centerx -= 1

    def flee(self):
        self.rect.centerx += self.direction
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH:
            self.kill()

    def destroy(self):
        self.timer -= 0.1
        if self.timer <= 0:
            self.kill()

    def update(self, enemy_list):
        self.animation_state()
        for enemy in enemy_list:
            if enemy.dead and not self.scared:
                self.scared = True
                if self.rect.centerx < enemy.rect.centerx:
                    self.direction *= -1
                break
        if self.in_love:
            pass
        elif not self.scared:
            self.move()
        else:
            self.flee()
        self.destroy()


class Lady(Citizen):

    def __init__(self):
        super().__init__()


class Grandma(Citizen):

    def __init__(self):
        super().__init__()
        frame_1 = pygame.image.load("assets/grandma/grandma-1.png").convert_alpha()
        frame_2 = pygame.image.load("assets/grandma/grandma-2.png").convert_alpha()

        self.frames = [frame_1, frame_2]
        self.index = 0

        self.image = self.frames[self.index]
        self.spawn_x = random.randint(50, SCREEN_WIDTH - 50)
        self.spawn_y = random.randint(50, SCREEN_HEIGHT - 50)
        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))


class BeardedMan(Citizen):

    def __init__(self):
        super().__init__()
        frame_1 = pygame.image.load("assets/bearded_man/bearded_man-1.png").convert_alpha()
        frame_2 = pygame.image.load("assets/bearded_man/bearded_man-2.png").convert_alpha()

        self.frames = [frame_1, frame_2]
        self.index = 0

        self.image = self.frames[self.index]
        self.spawn_x = random.randint(50, SCREEN_WIDTH - 50)
        self.spawn_y = random.randint(50, SCREEN_HEIGHT - 50)
        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))