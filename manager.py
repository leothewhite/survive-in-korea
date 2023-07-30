import pygame
import random


def input_manager(event, dt):
    speed = 0.2
    down_left, down_right, to_x = False, False, 0
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            to_x -= speed * 3 * dt
            down_left = True

        if event.key == pygame.K_RIGHT:
            to_x += speed * 3 * dt
            down_right = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            down_left = False
        if event.key == pygame.K_RIGHT:
            down_right = False

    return down_left, down_right, to_x


def background_manager(bg_y, place_idx, place_now_set, places, borders, dt):
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
    return place_now, bg_y, place_idx, place_now_set
