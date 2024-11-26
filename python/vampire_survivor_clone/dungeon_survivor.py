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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.bg_tile = pygame.image.load("images/background.png")
        self.tile_size = 1000

        # self.player = Player(400, 300)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.blit(self.bg_tile, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
