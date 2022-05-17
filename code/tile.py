import pygame
from settings import TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)

        self.type = type
        self.image = surface

        if type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILE_SIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)

        self.hit_area = self.rect.inflate(0, -10)