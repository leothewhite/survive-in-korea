import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()

    def update(self, pos):
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
    def __init__(self, img, name, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.name = name
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


class ManageVariable:
    _instance = None

    def __new__(cls, *args, **kargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kargs)
        return cls._instance

    def __init__(self, *args, **kargs):
        pass
