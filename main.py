import pygame

from sprites import Character, Border
from variable import VariableXY, VariableLR

pygame.init()


size = VariableXY(640, 480)
player = VariableXY(
    320, 240, pygame.image.load("./resources/images/character/player.png")
)
player.sprite = Character(player.img)
key_down = VariableLR(False, False)
boundary = VariableLR(233, 614)
to_x = 0

background = pygame.image.load("./resources/images/background/background.png")
SCREEN = pygame.display.set_mode((size.x, size.y))
CLOCK = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
RUNNING = True
speed = 0.2
borders_left = []
borders_right = []

for i in range(16):
    now_y = i * 40
    border_img = pygame.image.load("./resources/images/object/border.png")
    l = Border(border_img, (214, now_y))
    r = Border(border_img, (614, now_y))
    borders_left.append(l)
    borders_right.append(r)
    all_sprites.add(l)
    all_sprites.add(r)

player.sprite.update((player.x, player.y))
all_sprites.add(player.sprite)

i = 0


def move_background():
    global i
    # 참고: https://www.askpython.com/python-modules/pygame-looping-background
    SCREEN.blit(background, (0, i))
    SCREEN.blit(background, (0, size.y + i))
    if i <= -size.y + 1:
        i = 0
    # 속도
    i -= 0.2 * dt


def input_manager(event):
    global to_x
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            to_x -= speed * 3 * dt
            key_down.left = True

        if event.key == pygame.K_RIGHT:
            to_x += speed * 3 * dt
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
        to_x -= speed * dt
    if key_down.right:
        to_x += speed * dt

    move_background()

    if pygame.Rect.collidelist(player.sprite.rect, borders_left) != -1:
        if to_x < 0:
            to_x = 0
    elif pygame.Rect.collidelist(player.sprite.rect, borders_right) != -1:
        if 0 < to_x:
            to_x = 0
    player.x += to_x
    player.sprite.update((player.x, player.y))
    all_sprites.draw(SCREEN)
    to_x = 0

    pygame.display.update()


pygame.quit()
