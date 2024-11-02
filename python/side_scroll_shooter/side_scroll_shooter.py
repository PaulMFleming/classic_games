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

pygame .init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()

running = True

while running:
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE or event.key == K_q:
        running = False
    elif event.type == QUIT:
      running = False

  screen.fill((0, 0, 0))

  surf = pygame.Surface((50, 50))
  surf.fill((255, 255, 255))
  rect = surf.get_rect()

  surf_center = (
    (SCREEN_WIDTH-surf.get_width())/2,
    (SCREEN_HEIGHT-surf.get_height())/2
  )

  screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
  
  pygame.display.flip()
