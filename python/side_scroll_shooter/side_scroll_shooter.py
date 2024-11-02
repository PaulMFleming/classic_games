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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
