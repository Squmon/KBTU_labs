import pygame
import random
import time

pygame.init() # initializes all the pygame sub-modules

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creating a game window
# set_mode() takes a tuple as an argument

image_background = pygame.image.load('resources/AnimatedStreet.png')
image_player = pygame.image.load('resources/Player.png')
image_enemy = pygame.image.load('resources/Enemy.png')
image_coin = pygame.image.load('resources/coin.png')

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound('resources/crash.wav')
sound_coin = pygame.mixer.Sound('resources/coin.wav')

font = pygame.font.SysFont("Verdana", 60)
image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))

font_small = pygame.font.SysFont("Verdana", 20) # для счетчика

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5
        # or
        # self.rect.midbottom = (WIDTH // 2, HEIGHT)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

collected_coins = 0
score = 0

bg_speed = 10
class coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_coin
        self.rect = self.image.get_rect()
        self.speed = bg_speed

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = bg_speed
        # or
        # self.rect.midbottom = (WIDTH // 2, HEIGHT)

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        global score
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT + self.image.get_height():
            score += 1
            self.generate_random_rect()
            self.speed = random.randint(0, 10) + bg_speed

running = True

# this object allows us to set the FPS
clock = pygame.time.Clock()
FPS = 60

player = Player()
enemy = Enemy()
coin_count = 3
coins = [coin() for _ in range(coin_count)]
for c in coins: c.generate_random_rect()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy, *coins)
coin_sprites.add(*coins)
enemy_sprites.add(enemy)

position = 0
position2 = -image_background.get_height()
while running: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            running = False

    player.move()


    # двигаем дорогу
    screen.blit(image_background, (0, position))
    screen.blit(image_background, (0, position2))
    position += bg_speed
    position2 += bg_speed
    if position > HEIGHT:
        position = -image_background.get_height()

    if position2 > HEIGHT:
        position2 = -image_background.get_height()

    #рисуем скор по монеткам
    scores = font_small.render(str(collected_coins), True, YELLOW)
    screen.blit(scores, (WIDTH - 10 - scores.get_width(), 10))

    #рисуем скор по монеткам
    scores = font_small.render(str(score), True, BLACK)
    screen.blit(scores, (10, 10))

    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        running = False
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()

        time.sleep(3)

    if (q := pygame.sprite.spritecollideany(player, coin_sprites)):
        collected_coins += 1
        q.generate_random_rect()
        sound_coin.play()
        
    
    pygame.display.flip() # updates the screen
    clock.tick(FPS) # sets the FPS

pygame.quit()