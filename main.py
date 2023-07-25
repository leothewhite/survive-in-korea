import pygame
from sprites import Player
# from play import game_play
pygame.init()

width = 640
height = 480
SCREEN = pygame.display.set_mode((width, height))
bg = pygame.image.load("./resources/images/background/background.png")
player_img = pygame.image.load("./resources/images/character/player.png")
CLOCK = pygame.time.Clock()
RUNNING = True
player_x = 320
player_y = 240
i = 0

player = Player(player_img)
player.update((player_x, player_y))
all_sprites = pygame.sprite.Group(player)

while RUNNING:
    dt = CLOCK.tick(60)
    print(f"fps: {dt}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # 참고: https://www.askpython.com/python-modules/pygame-looping-background
    SCREEN.blit(bg, (0, i))
    SCREEN.blit(bg, (0, height+i))
    if (i <= -height+1):
        i = 0
    # 속도
    i -= 0.2*dt
    player.update((player_x, player_y))
    all_sprites.draw(SCREEN)
    
    pygame.display.update()

pygame.quit()