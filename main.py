import pygame
import os

from property import Character, Border, Place, Guage, ManageVariable
from manager import (
    background_manager,
    guage_manager,
    input_manager,
    collide_manager,
    load_border,
    load_images,
)

pygame.init()

intl = ManageVariable()

intl.size_x, intl.size_y = 640, 480
intl.player_x = 320
intl.to_x = 0
intl.gravity = 1
intl.guage = Guage()
intl.down_left, intl.down_right = False, False
intl.all_sprites = pygame.sprite.Group()
intl.SCREEN = pygame.display.set_mode((intl.size_x, intl.size_y))
intl.speed = 0.2
intl.borders = [[], [], [], []]
intl.places = {"a": [], "b": [], "c": []}
intl.place_cnt = {}
intl.bg_y = 0
intl.place_now_set = [-1, -1, -1]
intl.place_idx = 3


load_images()
load_border()

CLOCK = pygame.time.Clock()
RUNNING = True

intl.player = Character(intl.images["player"])
intl.place_now = intl.places["a"][0]

intl.player.update((intl.player_x, 240))
intl.all_sprites.add(intl.player)


while RUNNING:
    intl.dt = CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        input_manager(event)

    if intl.down_left:
        intl.to_x -= intl.speed * intl.dt
    if intl.down_right:
        intl.to_x += intl.speed * intl.dt

    if intl.place_now.rect.y - 40 <= intl.player.rect.y <= intl.place_now.rect.y + 200:
        intl.to_x -= intl.gravity

    background_manager()
    collide_manager()
    guage_manager()

    intl.player_x += intl.to_x

    intl.player.update((intl.player_x, 240))
    intl.all_sprites.draw(intl.SCREEN)
    intl.to_x = 0

    pygame.display.update()


pygame.quit()
