import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
    K_q,
)

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

score = 0
player_lives = 3

font = pygame.font.Font(None, 36)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/ship.png").convert()
        self.surf.set_colorkey((0, 0, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        laser = Laser(self.rect.centerx, self.rect.centery)
        lasers.add(laser)
        all_sprites.add(laser)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/enemy_A.png").convert()
        self.surf.set_colorkey((0, 0, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super(Meteor, self).__init__()
        self.surf = pygame.image.load("images/meteor_detailedLarge.png").convert()
        self.surf.set_colorkey((0, 0, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.surf = pygame.image.load("images/laserBlue.png").convert()
        self.surf.set_colorkey((0, 0, 255))
        self.rect = self.surf.get_rect(center=(x + 40, y))

    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDMETEOR = pygame.USEREVENT + 2
pygame.time.set_timer(ADDMETEOR, 1000)

player = Player()

enemies = pygame.sprite.Group()
lasers = pygame.sprite.Group()
meteors = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                running = False
            elif event.key == K_SPACE:
                player.shoot()
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            obstacles.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDMETEOR:
            new_meteor = Meteor()
            meteors.add(new_meteor)
            obstacles.add(new_meteor)
            all_sprites.add(new_meteor)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    lasers.update()
    meteors.update()

    for laser in lasers:
        enemy_hit = pygame.sprite.spritecollideany(laser, enemies)
        meteor_hit = pygame.sprite.spritecollideany(laser, meteors)
        if enemy_hit:
            enemy_hit.kill()
            laser.kill()
            score += 1

        if meteor_hit:
            laser.kill()

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, obstacles):
        player.kill()
        player_lives -= 1
        if player_lives > 0:
            pygame.time.wait(1000)
            player = Player()
            all_sprites.add(player)
        else:
            running = False

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (880, 40))

    lives_text = font.render(f"Lives: {player_lives}", True, (255, 255, 255))
    screen.blit(lives_text, (880, 10))

    pygame.display.flip()
    clock.tick(30)
