import pygame

from property import *
from manager import *
from scene import game_scene, menu_scene, over_scene

pygame.init()

CLOCK = pygame.time.Clock()
RUNNING = True

now_scene = "MENU"

while RUNNING:
    manager.dt = CLOCK.tick(60)

    if now_scene == "MENU":
        RUNNING, now_scene = menu_scene()

    if now_scene == "GAME":
        RUNNING, now_scene = game_scene()

    if now_scene[:4] == "OVER":
        RUNNING, now_scene = over_scene(now_scene.split()[1])

pygame.quit()
