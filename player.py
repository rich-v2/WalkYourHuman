import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

MAX_DISTANCE = 150
BASE_SPEED = 4
SIC_TIME = 100


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        dog_sit1 = pygame.image.load('assets/player/dog_sit_front-1.png').convert_alpha()
        # dog_sit1 = pygame.transform.rotozoom(dog_sit1, 0, 1)
        dog_sit2 = pygame.image.load('assets/player/dog_sit_front-2.png').convert_alpha()
        # dog_sit2 = pygame.transform.rotozoom(dog_sit2, 0, 1)

        self.sit_frames = [dog_sit1, dog_sit2]
        self.sit_index = 0
        self.bark_sound = pygame.mixer.Sound("music/dog_bark.mp3")
        self.image = self.sit_frames[self.sit_index]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.speed = BASE_SPEED
        self.sic = True
        self.sic_timer = 0
        self.sic_sound = pygame.mixer.Sound("music/dog_snarl.mp3")
        self.caught = False
        self.caught_timer = 0
        self.poop = 2
        self.pugs = 0
        self.donkey = 1
        self.win = False

    def distance_human(self, human):
        player_x, player_y = self.rect.center
        human_x, human_y = human.sprite.rect.center
        dist_x = human_x - player_x
        dist_y = human_y - player_y

        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

        if distance > MAX_DISTANCE:
            return False
        else:
            return True

    def move(self):
        if not self.caught:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if self.rect.top > 0:
                    self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                if self.rect.bottom < SCREEN_HEIGHT:
                    self.rect.y += self.speed
            if keys[pygame.K_LEFT]:
                if self.rect.left > 0:
                    self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                if self.rect.right < SCREEN_WIDTH:
                    self.rect.x += self.speed

    def animation_state(self):
        self.sit_index += 0.1
        if self.sit_index > len(self.sit_frames):
            self.sit_index = 0
        self.image = self.sit_frames[int(self.sit_index)]

    def bark(self, enemy_group):
        if pygame.key.get_pressed()[pygame.K_q]:
            for enemy in enemy_group:
                if not enemy.scared:
                    dist_x = enemy.rect.x - self.rect.x
                    dist_y = enemy.rect.y - self.rect.y

                    distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

                    if distance < 100 and not enemy.dead:
                        enemy.scared = True
                        enemy.scared_timer = 50
                        enemy.rect.x += 100 * enemy.speed * dist_x / distance
                        enemy.rect.y += 100 * enemy.speed * dist_y / distance
            self.bark_sound.play()

    def sic_enemy(self):
        if self.sic_timer < SIC_TIME:
            self.sic = False
        if not self.sic:
            self.sic_timer += 1
            if self.sic_timer > SIC_TIME:
                self.sic_timer = SIC_TIME
                self.sic = True

        else:
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.sic_timer == SIC_TIME:
                self.sic_sound.play()
                self.sic_timer = 0

    def call_animal_companions(self):
        self.pugs += 0.005
        if self.pugs > 2:
            self.pugs = 2

    def update(self, human, enemy_group):
        self.animation_state()
        self.call_animal_companions()
        if not self.caught:
            if self.distance_human(human):
                self.move()
            self.sic_enemy()
            self.bark(enemy_group)
        else:
            self.caught_timer -= 0.1
            if self.caught_timer <= 0:
                self.caught = False
