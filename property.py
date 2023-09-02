import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.images = []

        self.images += [
            pygame.image.load("./resources/images/character/player1.png")
        ] * 8
        self.images += [
            pygame.image.load("./resources/images/character/player2.png")
        ] * 8
        self.images += [
            pygame.image.load("./resources/images/character/player3.png")
        ] * 8
        self.images += [
            pygame.image.load("./resources/images/character/player4.png")
        ] * 8

        print(self.images)

        self.index = 0

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.index += 1

        if 32 <= self.index:
            self.index = 0

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Border(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Place(pygame.sprite.Sprite):
    def __init__(self, img, name, pos, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.name = name
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Guage:
    def __init__(self):
        self.stress = 20
        self.grade = 50
        self.future = 0
        self.health = 100


# * 전역 변수를 관리하기 윈한 싱글톤 클래스
class ManageVariable:
    _instance = None

    def __new__(cls, *args, **kargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kargs)
        return cls._instance

    def __init__(self, *args, **kargs):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Size:
    def __init__(self, width, height):
        self.x = width
        self.y = height


class MenuBackground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.backgrounds = []
        for i in range(1, 13):
            for _ in range(60):
                self.backgrounds.append(
                    pygame.image.load(f"./resources/images/menu/background{i}.png")
                )
        self.index = 0

        self.image = self.backgrounds[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        self.index += 1

        if 720 <= self.index:
            self.index = 0

        self.image = self.backgrounds[self.index]
        self.rect = self.image.get_rect()
