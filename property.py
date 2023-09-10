import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = []

        # 속도 조절 위해 한 프레임당 8번씩 들어감
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

        self.index = 0

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def update(self, pos):
        # self.index를 1씩 증가 시키며, 스프라이트의 이미지를 현재 인덱스의 이미지로 바꿔준다
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
        self.grade = 70
        self.future = 0
        self.health = 100


# 싱글턴 클래스
class ManageVariable:
    _instance = None

    def __new__(cls, *args, **kargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kargs)
        return cls._instance

    def __init__(self, *args, **kargs):
        pass


class MenuBackground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.backgrounds = []
        # 속도 조절 위해서 한 프레임당 60번씩 들어감
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
