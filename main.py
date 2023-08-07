import pygame
import os
import random

from property import Character, Border, Place, Guage, ManageVariable
from manager import move_background

pygame.init()

intl = ManageVariable()

intl.size_x, intl.size_y = 640, 480
player_x = 320
to_x = 0
gravity = 1

place_path = "./resources/images/place/"
guage_path = "./resources/images/guage/"
intl.images = {
    "player": pygame.image.load("./resources/images/character/player.png"),
    "border": pygame.image.load("./resources/images/background/border.png"),
    "background": pygame.image.load("./resources/images/background/background.png"),
    "place": [
        (i.split(".")[0], pygame.image.load(place_path + i))
        for i in os.listdir(place_path)
    ],
    "guage": {
        i.split(".")[0]: pygame.image.load(guage_path + i)
        for i in os.listdir(guage_path)
        if i != ".DS_Store"
    },
}

guage = Guage()

down_left, down_right = False, False

all_sprites = pygame.sprite.Group()


intl.SCREEN = pygame.display.set_mode((intl.size_x, intl.size_y))
CLOCK = pygame.time.Clock()
RUNNING = True

speed = 0.2

intl.borders = [[], [], [], []]
# a: 놀기 b: 공부 c: 취미
intl.places = {"a": [], "b": [], "c": []}
place_cnt = {}

player = Character(intl.images["player"])

for i in range(32):
    now_y = i * 60
    block = [
        Border(intl.images["border"], (171, now_y)),
        Border(intl.images["border"], (171, intl.size_y + now_y)),
        Border(intl.images["border"], (456, now_y)),
        Border(intl.images["border"], (456, intl.size_y + now_y)),
    ]
    for i in range(4):
        intl.borders[i].append(block[i])
        all_sprites.add(block[i])

for i, v in enumerate(intl.images["place"]):
    file_name = v[0]
    file = v[1]
    intl.places[v[0][0]].append(Place(file, file_name[2:], (33, intl.size_y)))
    place_cnt[file_name[2:]] = 0


intl.place_now_set = [-1, -1, -1]
place_now = intl.places["a"][0]
intl.place_idx = 3

player.update((player_x, 240))
all_sprites.add(player)

intl.bg_y = 0


def input_manager(event):
    global to_x, down_left, down_right
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            to_x -= speed * 3 * intl.dt
            down_left = True

        if event.key == pygame.K_RIGHT:
            to_x += speed * 3 * intl.dt
            down_right = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            down_left = False
        if event.key == pygame.K_RIGHT:
            down_right = False


def chk_collide(a, b):
    return pygame.Rect.collidelist(a, b)


def place_collide(player, place_type):
    col = chk_collide(player.rect, intl.places[place_type]) + 1
    if col:
        return intl.places[place_type][col - 1].name
    else:
        return False


def draw_guage():
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 440))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 400))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 360))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 320))

    for i in range(20):
        if guage.health // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["health"], (527 + 5 * i, 322))

    for i in range(20):
        if guage.future // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["future"], (527 + 5 * i, 362))

    for i in range(20):
        if guage.stress // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["stress"], (527 + 5 * i, 402))

    for i in range(20):
        if guage.grade // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["grade"], (527 + 5 * i, 442))


while RUNNING:
    intl.dt = CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        input_manager(event)
    if down_left:
        to_x -= speed * intl.dt
    if down_right:
        to_x += speed * intl.dt

    move_background()

    if place_now.rect.y - 40 <= player.rect.y <= place_now.rect.y + 200:
        to_x -= gravity

    if (
        chk_collide(player.rect, intl.borders[0]) + 1
        or chk_collide(player.rect, intl.borders[1]) + 1
    ):
        if to_x < 0:
            to_x = 0
    elif (
        chk_collide(player.rect, intl.borders[2]) + 1
        or chk_collide(player.rect, intl.borders[3]) + 1
    ):
        if 0 < to_x:
            to_x = 0

    # # 스트레스 풀기
    col_place = place_collide(player, "a")
    if col_place:
        guage.stress -= 5
        place_cnt[col_place] += 1
        if col_place == "alley":
            guage.health -= 5
        if col_place == "basketball":
            guage.health += 5
        if 3 <= place_cnt[col_place]:
            guage.grade -= 5

        player_x = 320

    col_place = place_collide(player, "b")
    if col_place:
        guage.stress += 5
        guage.grade += 5
        player_x = 320

    col_place = place_collide(player, "c")
    if col_place:
        guage.stress -= 5
        guage.future += 5
        player_x = 320

    draw_guage()
    player_x += to_x
    player.update((player_x, 240))
    all_sprites.draw(intl.SCREEN)
    to_x = 0

    pygame.display.update()


pygame.quit()
