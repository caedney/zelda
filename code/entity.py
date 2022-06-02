import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hit_area.x += self.direction.x * speed
        self.collision('horizontal')
        self.hit_area.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hit_area.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hit_area.colliderect(self.hit_area):
                    if self.direction.x > 0:  # moving right
                        self.hit_area.right = sprite.hit_area.left
                    if self.direction.x < 0:  # moving left
                        self.hit_area.left = sprite.hit_area.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hit_area.colliderect(self.hit_area):
                    if self.direction.y > 0:  # moving down
                        self.hit_area.bottom = sprite.hit_area.top
                    if self.direction.y < 0:  # moving up
                        self.hit_area.top = sprite.hit_area.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())

        if value >= 0:
            return 255
        else:
            return 0