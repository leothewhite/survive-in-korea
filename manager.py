import random
from constants import *
import pygame
from property import *

pygame.font.init()

manager = ManageVariable()


def background_manager():
    manager.bg_y -= 0.15 * manager.dt

    for idx in range(50):
        if 15 <= idx < 23:
            if 2 < manager.place_idx:
                if 3 == manager.now_place_cnt:
                    manager.guage.health -= 10

                for i in range(3):
                    manager.place_now_set[i] = random.choice(PLACES[chr(i + 97)])
                random.shuffle(manager.place_now_set)

                manager.place_idx = 0
                manager.now_place_cnt = 0

                manager.month += 1
                manager.isText = 1
                manager.now_alpha += manager.dt

            for t in range(2, 4):
                now = manager.borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 32))

            manager.place_now = manager.place_now_set[manager.place_idx]
            manager.place_now.update((0, manager.bg_y + SCREEN_SIZE[1]))

        else:
            for t in range(4):
                now = manager.borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 32))

    if manager.bg_y <= -(640 + 256):
        manager.bg_y = 0

        manager.place_idx += 1


def ending_manager():
    if manager.guage.stress == 100:
        return "stress"
    if manager.guage.health == 0:
        return "health"

    if 1 < manager.month:
        if manager.guage.grade < 30:
            return "grade"
        elif manager.guage.future < 50:
            return "future"
        else:
            return "happy"

    return False


def event_handler(event):
    if event.type == manager.place_timer:
        manager.inPlace = False

        manager.player_x = 480
        manager.bg_y = -400
        manager.player.update((manager.player_x, SCREEN_SIZE[1] / 2))

        manager.all_sprites.add(manager.player)
        manager.all_sprites.draw(manager.SCREEN)

        pygame.time.set_timer(manager.place_timer, 0)

    if not manager.inPlace:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                manager.to_x -= SPEED * 3 * manager.dt
                manager.down[0] = True

            if event.key == pygame.K_RIGHT:
                manager.to_x += SPEED * 3 * manager.dt
                manager.down[1] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                manager.down[0] = False
            if event.key == pygame.K_RIGHT:
                manager.down[1] = False


def is_collided(a, b):
    return pygame.Rect.collidelist(a, b)


def list_collided(player, place_type):
    col = is_collided(player.rect, PLACES[place_type]) + 1
    if col:
        return PLACES[place_type][col - 1].name
    else:
        return False


def guage_manager(place_type, col_place):
    if place_type == "a":
        manager.guage.stress -= 5
        if col_place == "alley":
            manager.guage.health -= 5
        if col_place == "basketball":
            manager.guage.health += 5
        if 5 <= manager.stress_cnt:
            manager.guage.grade -= 5
            manager.stress_cnt = 0

    if place_type == "b":
        manager.guage.stress += 10
        manager.guage.grade += 5

    if place_type == "c":
        manager.guage.future += 10


def collide_manager():
    for key in PLACES:
        col_place = list_collided(manager.player, key)

        if col_place:
            manager.all_sprites.remove(manager.player)
            manager.down = [False, False]
            pygame.time.set_timer(manager.place_timer, 2000)

            manager.bg_y = -400
            manager.inPlace = True

            manager.now_place_cnt += 1

            guage_manager(key, col_place)


def make_gravity():
    if manager.place_now.type == "a" or manager.place_now.type == "c":
        manager.gravity = manager.guage.stress / 10

    elif manager.place_now.type == "b":
        manager.gravity = -(manager.guage.stress / 10)

    if (
        manager.place_now.rect.y - manager.player.rect.height
        <= manager.player.rect.y
        <= manager.place_now.rect.y + 200
    ):
        manager.to_x -= manager.gravity


def move_player():
    if not manager.inPlace:
        if manager.down[0]:
            manager.to_x -= SPEED * manager.dt
        if manager.down[1]:
            manager.to_x += SPEED * manager.dt


def text_handler():
    if manager.now_alpha != 0:
        if manager.isText == 1:
            manager.now_alpha += 1 * manager.dt
            if 1000 <= manager.now_alpha:
                manager.isText = 2
        if manager.isText == 2:
            manager.now_alpha -= 1 * manager.dt
            if manager.now_alpha <= 1:
                manager.now_alpha = 0
                manager.title = -1
                manager.isText = 0

    if manager.isText == 1 or manager.isText == 2:
        manager.title = FONT.render(
            SEMESTER[manager.month], True, pygame.Color(0, 0, 0)
        )
        manager.title.set_alpha(manager.now_alpha)
