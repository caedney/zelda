import pygame
from settings import WORLD_MAP, TILE_SIZE
from tile import Tile
from player import Player
from camera import Camera
from random import choice
from import_csv import import_csv
from import_images import import_images
from debug import debug


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
        layouts = {
            'boundary': import_csv('map/map_FloorBlocks.csv'),
            'grass': import_csv('map/map_Grass.csv'),
            'object': import_csv('map/map_Objects.csv'),
        }

        graphics = {
            'grass': import_images('graphics/grass'),
            'objects': import_images('graphics/objects'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE

                        if style == 'boundary':
                            Tile((x, y), [self.obstacles_sprites], 'invisible')

                        if style == 'grass':
                            random_grass_surface = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_surface)

                        if style == 'object':
                            object_surface = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'object', object_surface)

        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacles_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()
        # debug
        debug(self.player.status)
