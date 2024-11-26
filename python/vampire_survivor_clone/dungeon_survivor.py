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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/wizard_survivor_small.png")
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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.bg_tile = pygame.image.load("images/background.png")
        self.tile_size = 250

        self.player = Player(400, 300)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            for x in range(0, SCREEN_WIDTH, self.tile_size):
                for y in range(0, SCREEN_HEIGHT, self.tile_size):
                    self.screen.blit(self.bg_tile, (x, y))

            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys)

            self.screen.blit(self.bg_tile, (0, 0))
            self.screen.blit(self.player.surf, self.player.rect)
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
