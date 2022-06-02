import pygame
from settings import TILE_SIZE
from tile import Tile
from player import Player
from camera import Camera
from weapon import Weapon
from ui import UI
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

        # attack sprites
        self.current_attack = None

        # sprites setup
        self.create_map()

        # user interface
        self.ui = UI()

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

        self.player = Player(
            (2000, 1430),
            [self.visible_sprites],
            self.obstacles_sprites,
            self.create_attack,
            self.destroy_attack,
            self.create_magic,
        )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def create_magic(self, style, strength, cost):
        print(style, strength, cost)

    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
