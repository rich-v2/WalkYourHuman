import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class Human(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        human_1 = pygame.image.load('assets/human/human-1.png').convert_alpha()
        human_2 = pygame.image.load('assets/human/human-2.png').convert_alpha()
        human_4 = pygame.image.load('assets/human/human-4.png').convert_alpha()
        human_5 = pygame.image.load('assets/human/human-5.png').convert_alpha()

        self.stand_frames = [human_1, human_2, human_4, human_5]
        self.stand_index = 0
        self.image = self.stand_frames[self.stand_index]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.cholesterol = 150
        self.hp = 200
        self.dead = False
        self.speed = 1

    def animation_state(self):
        self.stand_index += 0.1
        if self.cholesterol > 150:
            if self.stand_index > 1:
                self.stand_index = 0
        else:
            if self.stand_index > 4 or self.stand_index < 2:
                self.stand_index = 2

        self.image = self.stand_frames[int(self.stand_index)]

    def move_to_player(self, player):
        dist_x = player.sprite.rect.centerx - self.rect.centerx
        dist_y = player.sprite.rect.centery - self.rect.centery

        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

        if distance > 50:
            self.rect.centerx += self.speed * dist_x / distance
            self.rect.centery += self.speed * dist_y / distance

    def change_cholesterol(self, amount=1):
        self.cholesterol += amount
        if self.cholesterol < 0:
            self.cholesterol = 0

    def set_speed(self):
        if self.cholesterol < 150:
            if self.speed < 4:
                self.speed = 4
        elif self.cholesterol < 250:
            self.speed = 3
        else:
            self.speed = 2

    def change_hp(self):
        if self.cholesterol < 100:
            self.hp -= 0.1
        else:
            self.hp += 0.1
            if self.hp > 200:
                self.hp = 200

        if self.hp == 0:
            self.dead = True

    def update(self, player):
        self.animation_state()
        self.set_speed()
        self.move_to_player(player)
        if self.cholesterol > 500:
            self.dead = True
        self.change_hp()
