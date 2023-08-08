from property import *
from manager import *


intl = ManageVariable()

intl.player_x = 320
intl.to_x = 0
intl.down_left, intl.down_right = False, False
intl.all_sprites = pygame.sprite.Group()
intl.SCREEN = pygame.display.set_mode((640, 480))
intl.speed = 0.2
intl.places = {"a": [], "b": [], "c": []}


load_images()
load_border()


intl.player = Character(intl.images["player"])
intl.place_now = intl.places["a"][0]

intl.player.update((intl.player_x, 240))
intl.all_sprites.add(intl.player)


def game_scene():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"
        isEsc = input_manager(event)

        if isEsc:
            return True, "MENU"

    if intl.down_left:
        intl.to_x -= intl.speed * intl.dt
    if intl.down_right:
        intl.to_x += intl.speed * intl.dt

    make_gravity()
    background_manager()
    collide_manager()
    guage_manager()

    intl.player_x += intl.to_x

    intl.player.update((intl.player_x, 240))
    intl.all_sprites.draw(intl.SCREEN)
    intl.to_x = 0

    pygame.display.update()

    return True, "GAME"


def menu_scene():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"
        input_manager(event)

    pygame.display.update()

    return True, "MENU"
