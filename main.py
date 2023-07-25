import pygame
from sprites import Player


pygame.init()


width       = 640
height      = 480
SCREEN      = pygame.display.set_mode((width, height))
bg          = pygame.image.load("./resources/images/background/background.png")
player_img  = pygame.image.load("./resources/images/character/player.png")
player_x    = 320
player_y    = 240
CLOCK       = pygame.time.Clock()
RUNNING     = True
i           = 0
all_sprites = pygame.sprite.Group()
player      = Player(player_img)
speed       = 0.2

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
    i -= speed * dt


while RUNNING:
    dt = CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    move_background()

    player.update((player_x, player_y))
    all_sprites.draw(SCREEN)

    pygame.display.update()


pygame.quit()
