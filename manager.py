import pygame


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
