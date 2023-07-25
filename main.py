import pygame
# from play import game_play
pygame.init()

width = 640
height = 480
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load("./resources/images/background/background.png")
clock = pygame.time.Clock()
running = True
i = 0

while running:
    dt = clock.tick(60)
    print(f"fps: {dt}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 참고: https://www.askpython.com/python-modules/pygame-looping-background
    screen.blit(bg, (0, i))
    screen.blit(bg, (0, height+i))
    if (i <= -height+1):
        i = 0
    # 속도
    i -= 0.2*dt

    pygame.display.update()

pygame.quit()