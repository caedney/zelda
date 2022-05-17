import pygame
from settings import WORLD_MAP, TILE_SIZE
from tile import Tile
from player import Player
from camera import Camera
# from debug import debug


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = Camera()
        self.obstacles_sprites = pygame.sprite.Group()

        # sprites setup
        self.create_map()

    def create_map(self):

        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                elif col == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)
                elif col == "":
                    pass

    def run(self):

        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

        # debug(self.player.direction)
