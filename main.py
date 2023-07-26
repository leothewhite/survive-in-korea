import pygame

from sprites import Character
from variable import VariableXY, VariableLR

pygame.init()


size = VariableXY(640, 480)
player = VariableXY(
    320, 240, pygame.image.load("./resources/images/character/player.png")
)
player.sprite = Character(player.img)
key_down = VariableLR(False, False)
boundary = VariableLR(233, 614)

background = pygame.image.load("./resources/images/background/background.png")
SCREEN = pygame.display.set_mode((size.x, size.y))
CLOCK = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
RUNNING = True
speed = 0.2

player.sprite.update((player.x, player.y))
all_sprites.add(player.sprite)


def move_background():
    i = 0
    # 참고: https://www.askpython.com/python-modules/pygame-looping-background
    SCREEN.blit(background, (0, i))
    SCREEN.blit(background, (0, size.y + i))
    if i <= -size.y + 1:
        i = 0
    # 속도
    i -= 0.2 * dt


def input_manager(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            if boundary.left < player.x:
                player.x -= speed * 3 * dt
                key_down.left = True

        if event.key == pygame.K_RIGHT:
            if player.x + 40 < boundary.right:
                player.x += speed * 3 * dt
                key_down.right = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            key_down.left = False
        if event.key == pygame.K_RIGHT:
            key_down.right = False


while RUNNING:
    dt = CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        input_manager(event)

    if key_down.left:
        player.x -= speed * dt
    if key_down.right:
        player.x += speed * dt

    if player.x <= boundary.left:
        key_down.left = False
    if boundary.right <= player.x + 40:
        key_down.right = False

    move_background()

    player.sprite.update((player.x, player.y))
    all_sprites.draw(SCREEN)

    pygame.display.update()


pygame.quit()
