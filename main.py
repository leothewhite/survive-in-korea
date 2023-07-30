import pygame
import os
import random
import manager

from sprites import *

pygame.init()


player_x = 320
to_x = 0

place_path = "./resources/images/place/"
images = {
    "player": pygame.image.load("./resources/images/character/player.png"),
    "border": pygame.image.load("./resources/images/background/border.png"),
    "background": pygame.image.load("./resources/images/background/background.png"),
    "place": [(i, pygame.image.load(place_path + i)) for i in os.listdir(place_path)],
}

down_left, down_right = False, False

all_sprites = pygame.sprite.Group()

SCREEN = pygame.display.set_mode((640, 480))
CLOCK = pygame.time.Clock()
RUNNING = True

speed = 0.2

# left1, left2, right1, right2
borders = [[], [], [], []]

# a: stress, b: study, c: dream
places = {"a": [], "b": [], "c": []}


player = Character(images["player"])

for i in range(32):
    now_y = i * 40
    blocks = [
        Border(images["border"], (214, now_y)),
        Border(images["border"], (214, 480 + now_y)),
        Border(images["border"], (614, now_y)),
        Border(images["border"], (614, 480 + now_y)),
    ]
    for idx, block in enumerate(blocks):
        borders[idx].append(block)
        all_sprites.add(block)

for idx, file in enumerate(images["place"]):
    file_name = file[0].split(".")
    places[file[0][0]].append(Place(file[1], file[0][2:], (33, 480)))


place_now_set = [-1, -1, -1]
place_idx = 3

player.update((player_x, 240))
all_sprites.add(player)

bg_y = 0


def background_manager(bg_y, place_idx):
    SCREEN.blit(images["background"], (0, bg_y))
    SCREEN.blit(images["background"], (0, 640 + bg_y))

    for idx in range(32):
        if 12 <= idx <= 16:
            if 2 < place_idx:
                for i in range(3):
                    place_now_set[i] = random.choice(places[chr(i + 97)])
                random.shuffle(place_now_set)
                place_idx = 0
            place_now = place_now_set[place_idx]
            place_now.update((33, bg_y + 480))

            for t in range(2, 4):
                now = borders[t][idx]
                now.update((now.rect.x, bg_y + idx * 40))
        else:
            for t in range(4):
                now = borders[t][idx]
                now.update((now.rect.x, bg_y + idx * 40))

    if bg_y <= -680:
        place_idx += 1
        bg_y = 0

    bg_y -= 0.15 * dt
    return place_now, bg_y, place_idx


def collision_manager(a, b):
    if pygame.Rect.collidelist(a, b) == -1:
        return False
    else:
        return True


while RUNNING:
    dt = CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        down_left, down_right, to_x = manager.input_manager(event, dt)

    if down_left:
        to_x -= speed * dt
    if down_right:
        to_x += speed * dt

    place_now, bg_y, place_idx = background_manager(bg_y, place_idx)

    if collision_manager(player.rect, borders[0]) or collision_manager(
        player.rect, borders[1]
    ):
        if to_x < 0:
            to_x = 0
    elif collision_manager(player.rect, borders[2]) or collision_manager(
        player.rect, borders[3]
    ):
        if 0 < to_x:
            to_x = 0

    player_x += to_x
    player.update((player_x, 240))
    place_now.draw(SCREEN)
    all_sprites.draw(SCREEN)
    to_x = 0

    pygame.display.update()


pygame.quit()
