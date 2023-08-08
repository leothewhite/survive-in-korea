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
        input_manager(event)

    if intl.down_left:
        intl.to_x -= intl.speed * intl.dt
    if intl.down_right:
        intl.to_x += intl.speed * intl.dt

    make_gravity()
    background_manager()
    collide_manager()
    isOver, reason = guage_manager()

    if isOver:
        return True, "OVER" + f" {reason}"

    intl.player_x += intl.to_x

    intl.player.update((intl.player_x, 240))
    intl.all_sprites.draw(intl.SCREEN)
    intl.to_x = 0

    pygame.display.update()

    return True, "GAME"


def menu_scene():
    all_sprites = pygame.sprite.Group()
    obj = {
        "background": pygame.image.load("./resources/images/menu/menu_background.png"),
        "start": Button(pygame.image.load("./resources/images/menu/game_start.png")),
        "exit": Button(pygame.image.load("./resources/images/menu/game_exit.png")),
    }

    obj["start"].update((200, 200))
    obj["exit"].update((200, 260))

    all_sprites.add(obj["start"])
    all_sprites.add(obj["exit"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if obj["start"].rect.collidepoint(x, y):
                print("start game")
                return True, "GAME"
            if obj["exit"].rect.collidepoint(x, y):
                print("exit game")
                return False, "END"

    intl.SCREEN.blit(obj["background"], (0, 0))

    all_sprites.draw(intl.SCREEN)

    pygame.display.update()

    return True, "MENU"


def over_scene(reason):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True, "MENU"

    over = pygame.image.load("./resources/images/menu/menu_dead.png")

    intl.SCREEN.blit(over, (0, 0))

    pygame.display.update()

    return True, "OVER " + reason
