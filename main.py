import pygame

from sprites import Player

pygame.init()


width = 640
height = 480
SCREEN = pygame.display.set_mode((width, height))
bg = pygame.image.load("./resources/images/background/background.png")
player_img = pygame.image.load("./resources/images/character/player.png")
player_x = 320
player_y = 240
CLOCK = pygame.time.Clock()
RUNNING = True
i = 0
all_sprites = pygame.sprite.Group()
player = Player(player_img)
speed = 0.2
left_down = False
right_down = False
bound_left = 233
bound_right = 614
left_start = 0
right_start = 0
player.update((player_x, player_y))
all_sprites.add(player)


def move_background():
    global i
    # 참고: https://www.askpython.com/python-modules/pygame-looping-background
    SCREEN.blit(bg, (0, i))
    SCREEN.blit(bg, (0, height + i))
    if i <= -height + 1:
        i = 0
    # 속도
    i -= 0.2 * dt


while RUNNING:
    dt = CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if bound_left < player_x - 21:
                    player_x -= speed * 3 * dt
                    left_down = True
            if event.key == pygame.K_RIGHT:
                if player_x + 21 < bound_right:
                    player_x += speed * 3 * dt
                    right_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_down = False
            if event.key == pygame.K_RIGHT:
                right_down = False

    if left_down:
        player_x -= speed * dt
    if right_down:
        player_x += speed * dt
    if player_x - 21 <= bound_left:
        left_down = False
    if bound_right <= player_x + 21:
        right_down = False

    move_background()
    print(player_x, player_y)
    player.update((player_x, player_y))
    all_sprites.draw(SCREEN)

    pygame.display.update()


pygame.quit()
