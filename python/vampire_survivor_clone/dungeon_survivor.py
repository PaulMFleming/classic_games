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


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
MAP_WIDTH = 4000
MAP_HEIGHT = 3000


#############################################
## Player ##
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/wizard_survivor_small.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.direction = "right"
        self.health = 100
        self.last_shot = pygame.time.get_ticks()
        self.shot_delay = 3000

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if self.direction != "left":
                self.direction = "left"
                self.surf = pygame.transform.flip(self.surf, True, False)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if self.direction != "right":
                self.direction = "right"
                self.surf = pygame.transform.flip(self.surf, True, False)

        # Keep player on the screen
        self.rect.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shot_delay:
            self.last_shot = current_time
            return self.attack()
        return None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def attack(self):
        fireball = Fireball(self.rect.x, self.rect.y, self.direction)
        print(
            f"Player attacking from {self.rect.centerx}, {self.rect.centery}"
        )  # Debug print
        return fireball


#############################################
## Enemies ##
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super(Zombie, self).__init__()
        self.surf = pygame.image.load("images/Zombie.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.direction = "right"
        self.speed = random.randint(1, 3)
        self.player = player
        self.health = 10

    def update(self):
        # Move the zombie toward the player
        if self.rect.x < self.player.rect.x:
            self.rect.move_ip(self.speed, 0)
        if self.rect.x > self.player.rect.x:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.y < self.player.rect.y:
            self.rect.move_ip(0, self.speed)
        if self.rect.y > self.player.rect.y:
            self.rect.move_ip(0, -self.speed)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    @staticmethod
    def spawn_zombie(player):
        zombie = Zombie(
            random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT), player
        )
        return zombie


#############################################
## Weapons ##
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super(Fireball, self).__init__()
        self.surf = pygame.image.load("images/fireball.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10
        self.damage = 10
        print(f"Fireball created at {x}, {y} going {direction}")  # Debug print

    def update(self):
        if self.direction == "right":
            self.rect.move_ip(self.speed, 0)
        if self.direction == "left":
            self.rect.move_ip(-self.speed, 0)
        if self.direction == "up":
            self.rect.move_ip(0, -self.speed)
        if self.direction == "down":
            self.rect.move_ip(0, self.speed)

        # Remove fireball when it leaves the screen
        if self.rect.right < 0 or self.rect.left > MAP_WIDTH:
            self.kill()
        if self.rect.top < 0 or self.rect.bottom > MAP_HEIGHT:
            self.kill()


#############################################
## Game ##
class Camera:
    def __init__(self, width, height):
        # camera is a rectangle that represents the portion of the game world that the player can see
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        else:
            return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # limit scrolling to the world size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Add debug font initialization
        self.debug_font = pygame.font.Font(None, 36)

        self.bg_tile = pygame.image.load("images/background.png")
        self.tile_size = self.bg_tile.get_width()

        self.player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)

        self.zombies = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()

        for _ in range(10):
            zombie = Zombie.spawn_zombie(self.player)
            self.zombies.add(zombie)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    running = False

            pressed_keys = pygame.key.get_pressed()

            new_fireball = self.player.update(pressed_keys)
            if new_fireball is not None:
                self.fireballs.add(new_fireball)
                print(f"Number of fireballs: {len(self.fireballs)}")  # Debug print

            # self.player.update(pressed_keys)

            self.zombies.update()
            self.fireballs.update()

            self.camera.update(self.player)

            # Tile the background
            for x in range(0, MAP_WIDTH, self.tile_size):
                for y in range(0, MAP_HEIGHT, self.tile_size):
                    self.screen.blit(
                        self.bg_tile,
                        self.camera.apply(
                            pygame.Rect(x, y, self.tile_size, self.tile_size)
                        ),
                    )

            self.screen.blit(self.player.surf, self.camera.apply(self.player))
            for zombie in self.zombies:
                self.screen.blit(zombie.surf, self.camera.apply(zombie))
            for fireball in self.fireballs:
                pygame.draw.rect(
                    self.screen, (255, 0, 0), self.camera.apply(fireball), 1
                )  # Debug rectangle
                self.screen.blit(fireball.surf, self.camera.apply(fireball))

            # Draw debug info
            debug_text = self.debug_font.render(
                f"Fireballs: {len(self.fireballs)}", True, (255, 255, 255)
            )
            self.screen.blit(debug_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
