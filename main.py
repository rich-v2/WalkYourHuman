import pygame
from sys import exit
import random

# Character Classes
from player import Player
from human import Human
from ice_vendor import IceVendor
from dog_catcher import DogCatcher
from burger_flinger import BurgerFlinger
from hoover import Hoover
from citizen import Lady, Grandma, BeardedMan
from dogs import Pug
# Environment
from tree import Tree
from house import House

# Items
from poop import Poop
from apple import Apple
from sausage import Sausage

# Game constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
MAX_SPEED = 8
score = 0
start_time = 0
current_time = 0
first_death = True
music_playing = "quirky"


def change_cholesterol(amount=1):
    """Change human cholesterol by amount and print change next to human on screen."""
    global screen
    human.sprite.change_cholesterol(amount)
    if amount > 0:
        chol_surf = text_font.render(f"+{human.sprite.cholesterol}", False, "red")
    else:
        chol_surf = text_font.render(f"-{human.sprite.cholesterol}", False, "blue")

    chol_rect = chol_surf.get_rect(midleft=human.sprite.rect.midright)
    screen.blit(chol_surf, chol_rect)


def collision_sprite():
    """Check for sprite collisions."""
    global score, first_death, music_playing
    # Events
    enemies_hit_player = pygame.sprite.spritecollide(player.sprite, enemy_list, False)
    enemies_hit_human = pygame.sprite.spritecollide(human.sprite, enemy_list, False)
    catcher_caught_dog = pygame.sprite.spritecollide(player.sprite, catcher_list, False)
    human_ate_apple = pygame.sprite.spritecollide(human.sprite, apple_list, False)
    dog_ate_sausage = pygame.sprite.spritecollide(player.sprite, sausage_list, False)

    if enemies_hit_player:
        for enemy in enemies_hit_player:
            if not enemy.dead and player.sprite.sic and pygame.key.get_pressed()[pygame.K_SPACE]:
                if first_death:
                    pygame.mixer.music.load("music/aggressive.mp3")
                    pygame.mixer.music.play()
                    first_death = False
                    music_playing = "aggressive"
                score -= 20
                wilhelm_scream.play()
                enemy.dead = True
                return None
    if enemies_hit_human:
        for enemy in enemies_hit_human:
            if not enemy.dead:
                change_cholesterol()

    if catcher_caught_dog:
        for catcher in catcher_caught_dog:
            if not catcher.dead:
                player.sprite.caught = True
                player.sprite.caught_timer = 10
                player.sprite.speed = 4
                catcher.dead = True
            return

    if human_ate_apple:
        for apple in human_ate_apple:
            apple_eating.play()
            apple.kill()
            change_cholesterol(amount=10)
            if human.sprite.speed < MAX_SPEED:
                human.sprite.speed += 0.1

    if dog_ate_sausage:
        for sausage in dog_ate_sausage:
            dog_panting.play()
            if player.sprite.speed < MAX_SPEED:
                player.sprite.speed += 0.1
            if player.sprite.poop <= 5:
                player.sprite.poop += 1
            sausage.kill()

    for enemy in enemy_list:
        if isinstance(enemy, BurgerFlinger):
            for patty in enemy.patties:
                human_x = human.sprite.rect.x
                human_y = human.sprite.rect.y
                width = human.sprite.rect.width
                height = human.sprite.rect.height
                if human_x < patty.x < human_x + width and human_y < patty.y < human_y + height:
                    human.sprite.cholesterol += 20
                    enemy.patties.pop(enemy.patties.index(patty))

                for pug in pug_list:
                    pug_x = pug.rect.x
                    pug_y = pug.rect.y
                    width = pug.rect.width
                    height = pug.rect.height
                    if pug_x < patty.x < pug_x + width and pug_y < patty.y < pug_y + height:
                        enemy.patties.pop(enemy.patties.index(patty))
                        break
                for house in house_list:
                    house_x = house.rect.x
                    house_y = house.rect.y
                    width = house.rect.width
                    height = house.rect.height
                    if house_x < patty.x < house_x + width and house_y < patty.y < house_y + height:
                        enemy.patties.pop(enemy.patties.index(patty))
                        break

    house_collision(player)
    house_collision(enemy_list)
    house_collision(pug_list)
    house_collision(catcher_list)
    house_collision(sausage_list)
    house_collision(apple_list)
    for house in house_list:
        pygame.sprite.spritecollide(house,citizen_list, dokill=True)


def house_collision(sprite_list):
    for house in house_list:
        if isinstance(sprite_list, pygame.sprite.GroupSingle):
            if pygame.sprite.spritecollide(house, sprite_list, dokill=False):
                dist_x = sprite_list.sprite.rect.centerx - house.rect.centerx
                dist_y = sprite_list.sprite.rect.centery - house.rect.centery
                hor = abs(dist_x) > abs(dist_y)
                if hor:
                    if dist_x < 0:
                        sprite_list.sprite.rect.right = house.rect.left
                    else:
                        sprite_list.sprite.rect.left = house.rect.right
                else:
                    if dist_y > 0:
                        sprite_list.sprite.rect.top = house.rect.bottom
                    else:
                        sprite_list.sprite.rect.bottom = house.rect.top
        else:
            collision_list = pygame.sprite.spritecollide(house, sprite_list, dokill=False)
            for character in collision_list:
                dist_x = character.rect.centerx - house.rect.centerx
                dist_y = character.rect.centery - house.rect.centery
                hor = abs(dist_x) > abs(dist_y)
                if hor:
                    if dist_x < 0:
                        character.rect.right = house.rect.left
                    else:
                        character.rect.left = house.rect.right
                else:
                    if dist_y > 0:
                        character.rect.top = house.rect.bottom
                    else:
                        character.rect.bottom = house.rect.top

def game_over():
    global enemy_list, catcher_list, hoover, poop_list, player
    if human.sprite.dead or player.sprite.win:
        enemy_list.empty()
        catcher_list.empty()
        hoover.empty()
        poop_list.empty()
        player.sprite.poop = 0
        return False
    return True


def increase_speed(enemy_list):
    if current_time > 200:
        for enemy in enemy_list:
            enemy.speed = 3
    elif current_time > 300:
        for enemy in enemy_list:
            enemy.speed = 4


def check_death(sprt_list):
    for sprt in sprt_list:
        if sprt.dead:
            return False
    return True



def display_boss_health():
    if len(hoover) > 0:
        for machine in hoover:
            display_x, display_y = machine.rect.midtop
            health_surf = text_font.render(f"{machine.hp}", False, "black")
            health_rect = health_surf.get_rect(midtop=(display_x, display_y - 20))
            screen.blit(health_surf, health_rect)


def display_stats():
    global score, start_time, current_time
    current_time = (pygame.time.get_ticks() - start_time) // 1000 + score
    score_surf = text_font.render(f"Score: {current_time}", False, "black")
    score_rect = score_surf.get_rect(topleft=(10, SCREEN_HEIGHT * 0.05))
    screen.blit(score_surf, score_rect)

    cholesterol_surf = text_font.render(f"Cholesterol: {human.sprite.cholesterol}", False, "black")
    cholesterol_rect = cholesterol_surf.get_rect(topleft=(10, SCREEN_HEIGHT * 0.1))
    screen.blit(cholesterol_surf, cholesterol_rect)

    hp_surf = text_font.render(f"Health: {int(human.sprite.hp)}", False, "black")
    hp_rect = hp_surf.get_rect(topleft=(10, SCREEN_HEIGHT * 0.15))
    screen.blit(hp_surf, hp_rect)

    poop_surf = text_font.render(f"Poop: {player.sprite.poop}", False, "black")
    poop_rect = poop_surf.get_rect(topleft=(10, SCREEN_HEIGHT * 0.2))
    screen.blit(poop_surf, poop_rect)

    pugs_surf = text_font.render(f"Pugs: {int(player.sprite.pugs)}", False, "black")
    pugs_rect = pugs_surf.get_rect(topleft=(10, SCREEN_HEIGHT * 0.25))
    screen.blit(pugs_surf, pugs_rect)

    sic_surf = text_font.render(f"Sic Timer: {player.sprite.sic_timer}", False, "black")
    sic_rect = sic_surf.get_rect(topleft=(10, SCREEN_HEIGHT * 0.3))
    screen.blit(sic_surf, sic_rect)


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Walk Your Human!")
background_surf = pygame.image.load("assets/background.png")
clock = pygame.time.Clock()
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)

pygame.mixer.music.load("music/a-little-quirky-167769.mp3")
pygame.mixer.music.play(loops=-1)
wilhelm_scream = pygame.mixer.Sound("music/wilhelm.mp3")
dog_panting = pygame.mixer.Sound("music/dog_panting.mp3")
dog_howl = pygame.mixer.Sound("music/howl.mp3")
apple_eating = pygame.mixer.Sound("music/apple_eating.mp3")
hoover_sound = pygame.mixer.Sound("music/hoover_sound.mp3")

# Groups
player = pygame.sprite.GroupSingle(Player())

human = pygame.sprite.GroupSingle(Human())

pug_list = pygame.sprite.Group()

enemy_list = pygame.sprite.Group()

hoover = pygame.sprite.Group()

catcher_list = pygame.sprite.Group()

citizen_list = pygame.sprite.Group()

tree_list = pygame.sprite.Group()

poop_list = pygame.sprite.Group()

apple_list = pygame.sprite.Group()
sausage_list = pygame.sprite.Group()

for i in range(100):
    spawn_x = random.randint(0, SCREEN_WIDTH)
    spawn_y = (SCREEN_HEIGHT / 100) * i
    tree_list.add(Tree(spawn_x, spawn_y))

house_list = pygame.sprite.Group()
for j in range(4):
    spawn_x = random.randint(100, SCREEN_WIDTH - 100)
    spawn_y = random.randint(100, SCREEN_HEIGHT - 100)
    house_list.add(House(spawn_x, spawn_y))

for house in house_list:
    pygame.sprite.spritecollide(house, tree_list, dokill= True)

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2000)

catcher_timer = pygame.USEREVENT + 2
pygame.time.set_timer(catcher_timer, 10000)

cholesterol_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cholesterol_timer, 500)

apple_timer = pygame.USEREVENT + 4
pygame.time.set_timer(apple_timer, 7000)

sausage_timer = pygame.USEREVENT + 5
pygame.time.set_timer(sausage_timer, 4000)

hoover_timer = pygame.USEREVENT + 6
pygame.time.set_timer(hoover_timer, 5000)

citizen_timer = pygame.USEREVENT + 7
pygame.time.set_timer(citizen_timer, 1000)

game_on = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not player.sprite.win:
            if game_on:
                if event.type == enemy_timer:
                    if random.randint(0, 3) <= 2:
                        enemy_list.add(IceVendor())
                    else:
                        enemy_list.add(BurgerFlinger())
                if event.type == catcher_timer:
                    if current_time < 0:
                        catcher_list.add(DogCatcher())
                if event.type == cholesterol_timer:
                    change_cholesterol(-1)
                if event.type == apple_timer:
                    apple_list.add(Apple())
                if event.type == sausage_timer:
                    sausage_list.add(Sausage())
                if event.type == hoover_timer:
                    if current_time > 100 and len(hoover) == 0:
                        pygame.mixer.music.load("music/boss_theme.mp3")
                        pygame.mixer.music.play()
                        hoover_sound.play()
                        hoover.add(Hoover())
                if event.type == citizen_timer:
                    who = random.choice(["lady", "grandma", "beardedman"])
                    if who == "lady":
                        citizen_list.add(Lady())
                    if who == "beardedman":
                        citizen_list.add(BeardedMan())
                    else:
                        citizen_list.add(Grandma())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if player.sprite.poop > 0:
                            player.sprite.poop -= 1
                            poop_list.add(Poop(player.sprite.rect.center))
                    if event.key == pygame.K_a:
                        if int(player.sprite.pugs) > 0 and not player.sprite.caught:
                            dog_howl.play()
                            player.sprite.pugs -= 1
                            pug_list.add(Pug(player.sprite.rect.centerx, player.sprite.rect.centery))

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        human.sprite.dead = False
                        human.sprite.cholesterol = 150
                        start_time = pygame.time.get_ticks()
                        score = 0
                        game_on = True
                        pygame.mixer.music.load("music/a-little-quirky-167769.mp3")
                        pygame.mixer.music.play()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over()
                    human.sprite.dead = False
                    human.sprite.cholesterol = 150
                    start_time = pygame.time.get_ticks()
                    score = 0
                    game_on = True
                    player.sprite.win = False
                    pygame.mixer.music.load("music/a-little-quirky-167769.mp3")
                    hoover_sound.stop()
                    pygame.mixer.music.play()
    if not player.sprite.win:
        if game_on:
            if human.sprite.cholesterol < 100:
                screen.fill("blue")
            else:
                screen.fill("#4aeba1")

            house_list.draw(screen)

            increase_speed(enemy_list)
            enemy_list.update(human, screen)
            enemy_list.draw(screen)

            pug_list.update(enemy_list)
            pug_list.draw(screen)

            human.update(player)
            human.draw(screen)
            if human.sprite.cholesterol < 150:
                leash_pos = human.sprite.rect.x + 40
            else:
                leash_pos = human.sprite.rect.x + 50
            pygame.draw.line(screen, "black", start_pos=(leash_pos, human.sprite.rect.y + 35), end_pos=player.sprite.rect.center)
            player.update(human, enemy_list)
            player.draw(screen)

            catcher_list.update(player)
            catcher_list.draw(screen)

            hoover.update(player, poop_list)
            hoover.draw(screen)
            display_boss_health()

            apple_list.update()
            apple_list.draw(screen)

            poop_list.draw(screen)
            poop_list.update(enemy_list, catcher_list)

            sausage_list.update()
            sausage_list.draw(screen)

            citizen_list.update(enemy_list)
            citizen_list.draw(screen)

            collision_sprite()

            tree_list.update()
            tree_list.draw(screen)

            game_on = game_over()

            display_stats()
            if music_playing == "aggressive" and not current_time < 0:
                all_alive = True
                for enemy in enemy_list:
                    if enemy.dead:
                        all_alive = False
                if all_alive:
                    first_death = True
                    pygame.mixer.music.load("music/a-little-quirky-167769.mp3")
                    pygame.mixer.music.play()
                    music_playing = "quirky"
        else:
            screen.fill("black")
            game_over_surf = text_font.render(f"Your human is dead. You killed {-score // 20} people.", False, "white")
            game_over_rect = game_over_surf.get_rect(midtop=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5))
            screen.blit(game_over_surf, game_over_rect)

            human_surf = pygame.image.load("assets/human/human-3.png").convert_alpha()
            human_surf = pygame.transform.rotozoom(human_surf, 90, 4)
            human_rect = human_surf.get_rect(midtop=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 5) * 2))
            screen.blit(human_surf, human_rect)

            play_again_surf = text_font.render(f" Your final score is {current_time}. Press 'Space' to Play Again", False, "white")
            play_again_rect = play_again_surf.get_rect(midtop=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 5) * 4))
            screen.blit(play_again_surf, play_again_rect)
    else:
        screen.fill("blue")
        win_surf = text_font.render("You win!", False, "white")
        win_rect = win_surf.get_rect(midtop=(SCREEN_WIDTH/2, SCREEN_HEIGHT/5))

        winner_surf = pygame.image.load("assets/player/dog_sit_front-1.png").convert_alpha()
        winner_surf = pygame.transform.rotozoom(winner_surf, 0, 4)
        winner_rect = winner_surf.get_rect(midtop = (2 * SCREEN_WIDTH / 5, 2.69 * SCREEN_HEIGHT / 5))

        winner2_surf = pygame.image.load("assets/human/human-4.png").convert_alpha()
        winner2_surf = pygame.transform.rotozoom(winner2_surf, 0, 4)
        winner2_rect = winner2_surf.get_rect(midtop=(3 * SCREEN_WIDTH / 5, 2 * SCREEN_HEIGHT / 5))

        play_again_surf = text_font.render(f" Your final score is {current_time}. Press 'Space' to Play Again", False,
                                           "white")
        play_again_rect = play_again_surf.get_rect(midtop=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 5) * 4))

        screen.blit(win_surf, win_rect)
        screen.blit(winner2_surf, winner2_rect)
        screen.blit(winner_surf, winner_rect)
        screen.blit(play_again_surf, play_again_rect)


    pygame.display.update()
    clock.tick(60)