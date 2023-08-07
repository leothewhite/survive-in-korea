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
    make_variable,
)

pygame.init()

intl = ManageVariable()

make_variable()
load_images()
load_border()


intl.player = Character(intl.images["player"])
intl.place_now = intl.places["a"][0]

intl.player.update((intl.player_x, 240))
intl.all_sprites.add(intl.player)


while intl.RUNNING:
    intl.dt = intl.CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intl.RUNNING = False
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
