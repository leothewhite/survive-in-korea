import random
from property import ManageVariable

intl = ManageVariable()


def move_background():
    intl.SCREEN.blit(intl.images["background"], (0, intl.bg_y))
    intl.SCREEN.blit(intl.images["background"], (0, 640 + intl.bg_y))
    for idx in range(32):
        if 12 <= idx < 16:
            if 2 < intl.place_idx:
                for i in range(3):
                    intl.place_now_set[i] = random.choice(intl.places[chr(i + 97)])
                random.shuffle(intl.place_now_set)
                intl.place_idx = 0
            place_now = intl.place_now_set[intl.place_idx]
            place_now.update((31, intl.bg_y + intl.size_y))
            place_now.draw(intl.SCREEN)
            for t in range(2, 4):
                now = intl.borders[t][idx]
                now.update((now.rect.x, intl.bg_y + idx * 40))
        else:
            for t in range(4):
                now = intl.borders[t][idx]
                now.update((now.rect.x, intl.bg_y + idx * 40))
    if intl.bg_y <= -intl.size_y - 160:
        intl.place_idx += 1
        bg_y = 0

    intl.bg_y -= 0.15 * intl.dt
