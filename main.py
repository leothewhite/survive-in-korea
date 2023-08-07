import pygame

from property import *
from manager import *
from scene import game_scene

pygame.init()

CLOCK = pygame.time.Clock()
RUNNING = True

now_scene = "GAME"

while RUNNING:
    intl.dt = CLOCK.tick(60)

    if now_scene == "GAME":
        RUNNING = game_scene()

pygame.quit()
