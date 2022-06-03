import pygame
from settings import TILE_SIZE
from tile import Tile
from player import Player
from enemy import Enemy
from camera import Camera
from weapon import Weapon
from ui import UI
from particle_animation import ParticleAnimation
from magic import Magic
from random import choice, randint
from import_csv import import_csv
from import_images import import_images


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = Camera()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprites setup
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.particle_animation = ParticleAnimation()
        self.magic = Magic(self.particle_animation)

    def create_map(self):
        layouts = {
            'boundary': import_csv('map/map_FloorBlocks.csv'),
            'grass': import_csv('map/map_Grass.csv'),
            'object': import_csv('map/map_Objects.csv'),
            'entities': import_csv('map/map_Entities.csv')
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
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
                                'grass',
                                random_grass_surface,
                            )

                        if style == 'object':
                            object_surface = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'object', object_surface)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacles_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                )
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                elif col == '393': monster_name = 'squid'

                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacles_sprites,
                                    self.damage_player,
                                    self.death_particles,
                                )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def player_attack(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collisions = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)

                if collisions:
                    for collision in collisions:
                        if collision.sprite_type == 'grass':
                            pos = collision.rect.center
                            offset = pygame.math.Vector2(0, 75)

                            for leaf in range(randint(3, 6)):
                                self.particle_animation.create_grass_particles(pos - offset, [self.visible_sprites])

                            collision.kill()

                        elif collision.sprite_type == 'enemy':
                            collision.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.particle_animation.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def death_particles(self, pos, particle_type):
        self.particle_animation.create_particles(particle_type, pos, [self.visible_sprites])

    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack()
        self.ui.display(self.player)
