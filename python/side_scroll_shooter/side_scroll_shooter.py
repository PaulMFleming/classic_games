import pygame
import random
import json
import os

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
high_score_file = "high_score.json"

font = pygame.font.Font(None, 36)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/ship.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
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

    def reset_position(self):
        self.rect.centerx = 10
        self.rect.centery = SCREEN_HEIGHT // 2


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/enemy_A.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
        self.dying = False
        self.flash_counter = 0

    def update(self):
        if self.dying:
            self.flash_counter += 1
            if self.flash_counter % 10 < 5:
                self.surf.set_alpha(0)
            else:
                self.surf.set_alpha(255)
            if self.flash_counter >= 10:
                self.kill()
        else:
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super(Meteor, self).__init__()
        self.surf = pygame.image.load("images/meteor_detailedLarge.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
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
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x + 40, y))

    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Explosion, self).__init__()
        self.images = []
        for i in range(9):
            img = pygame.image.load(f"images/simpleExplosion0{i}.png").convert()
            img.set_colorkey((0, 0, 0), RLEACCEL)
            self.images.append(img)
        self.index = 0
        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.animation_complete = False

    def update(self):
        if not self.animation_complete:
            explosion_speed = 2
            self.counter += 1
            if self.counter >= explosion_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.kill()
                else:
                    self.surf = self.images[self.index]
                    self.rect = self.surf.get_rect(center=self.rect.center)


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
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()


def read_high_score(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)["high_score"]
        except (json.JSONDecodeError, KeyError):
            return 0
    return 0


high_score = read_high_score(high_score_file)


def write_high_score(file_path, score):
    with open(file_path, "w") as file:
        json.dump({"high_score": score}, file)


# Menu loop

menu = True

while menu:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                menu = False
            elif event.key == K_SPACE:
                menu = False
        elif event.type == QUIT:
            menu = False

    high_score = read_high_score(high_score_file)

    screen.fill((0, 0, 0))
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("Space Shooter", True, (255, 255, 255))
    menu_text = font.render("Press SPACE to start", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(menu_text, (400, 400))
    screen.blit(title_text, (350, 200))
    screen.blit(high_score_text, (400, 300))

    pygame.display.flip()

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
    explosions.update()

    for laser in lasers:
        enemy_hit = pygame.sprite.spritecollideany(laser, enemies)
        meteor_hit = pygame.sprite.spritecollideany(laser, meteors)
        if enemy_hit:
            enemy_hit.dying = True
            laser.kill()
            score += 1

        if meteor_hit:
            laser.kill()

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        if entity != player:
            screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect)

    for explosion in explosions:
        screen.blit(explosion.surf, explosion.rect)

    if pygame.sprite.spritecollideany(player, obstacles):
        if player_lives > 0:
            explosion = Explosion(player.rect.centerx, player.rect.centery)
            explosions.add(explosion)
            all_sprites.add(explosion)
            player_lives -= 1
            player.reset_position()

            for obstacle in obstacles:
                if obstacle.rect.left < SCREEN_WIDTH // 2:
                    obstacle.kill()

        else:
            explosion = Explosion(player.rect.centerx, player.rect.centery)
            explosions.add(explosion)
            all_sprites.add(explosion)
            running = False

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (880, 40))

    lives_text = font.render(f"Lives: {player_lives}", True, (255, 255, 255))
    screen.blit(lives_text, (880, 10))

    pygame.display.flip()
    clock.tick(30)

if score > high_score:
    high_score = score
    write_high_score(high_score_file, score)


# Game over loop
game_over = True
while game_over:
    for event in pygame.event.get():
        if event.type == QUIT or (
            event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)
        ):
            game_over = False

    screen.fill((0, 0, 0))
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    screen.blit(game_over_text, (350, 200))
    screen.blit(high_score_text, (400, 400))
    screen.blit(score_text, (400, 300))

    pygame.display.flip()
