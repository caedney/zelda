import pygame
from entity import Entity
from import_images import import_images
from settings import *


class Enemy(Entity):
    def __init__(self, enemy_name, pos, groups, obstacle_sprites, damage_player):
        super().__init__(groups)

        self.sprite_type = 'enemy'

        # graphics
        self.import_enemy_assets(enemy_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hit_area = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.enemy_name = enemy_name
        enemy_info = ENEMY_DATA[self.enemy_name]
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.speed = enemy_info['speed']
        self.resistance = enemy_info['resistance']
        self.attack_damage = enemy_info['attack_damage']
        self.attack_type = enemy_info['attack_type']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_enemy_assets(self, name):
        self.animations = { 'idle': [], 'move': [], 'attack': [] }
        main_path = f'graphics/monsters/{name}/'

        for animation in self.animations.keys():
            self.animations[animation] = import_images(main_path + animation)

    def get_player_position(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_position(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0

            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_position(player)[1]

            if attack_type == 'weapon':
                self.health -= player.get_weapon_damage()
            else:
                pass  # magic damage

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False

            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hit_area.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_position(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def timers(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.timers()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)