import pygame
from settings import *
from random import randint


class Magic:
    def __init__(self, particle_animation):
        self.particle_animation = particle_animation

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost

            if player.health >= player.stats['health']:
                player.health = player.stats['health']

            self.particle_animation.create_particles('aura', player.rect.center, groups)
            self.particle_animation.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player, cost, groups):
        if player.energy >= -cost:
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            elif player.status.split('_')[0] == 'down':
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:
                    # horizontal
                    offset_x = (direction.x * i) * TILE_SIZE
                    x = player.rect.centerx + offset_x + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.particle_animation.create_particles('flame', (x, y), groups)
                else:
                    # vertical
                    offset_y = (direction.y * i) * TILE_SIZE
                    x = player.rect.centerx + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.particle_animation.create_particles('flame', (x, y), groups)
