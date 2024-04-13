import pygame


class Donkey(pygame.sprite.Sprite):

    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        frame_1 = pygame.image.load("assets/donkey/donkey-1.png").convert_alpha()
        frame_2 = pygame.image.load("assets/donkey/donkey-2.png").convert_alpha()
        self.frames = [frame_1, frame_2]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.heart = pygame.image.load("assets/donkey/heart-1.png")
        self.timer = 200

    def bewitch(self, sprt_list, win):
        for character in sprt_list:
            dist_x = character.rect.centerx - self.rect.centerx
            dist_y = character.rect.centery - self.rect.centery

            distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

            if distance < 200:
                if not character.in_love:
                    character.in_love = True
                    character.in_love_timer = 100
                if character.in_love:
                    win.blit(self.heart, character.rect.center)

    def animation_state(self):
        self.index += 0.1
        if self.index > len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def destroy(self):
        self.timer -= 0.1
        if self.timer <= 0:
            self.kill()

    def update(self, win, *args):
        self.animation_state()
        for li in args:
            self.bewitch(li, win)
        self.destroy()

