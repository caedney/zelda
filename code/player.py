import pygame
from entity import Entity
from settings import *
from import_images import import_images


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)

        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.status = 'down_idle'
        self.hit_area = self.rect.inflate(0, -24)
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # player assets
        self.import_player_assets()

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(MAGIC_DATA.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = { 'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5 }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 123

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        self.animations = {
            'up': [],
            'right': [],
            'down': [],
            'left': [],
            'up_idle': [],
            'right_idle': [],
            'down_idle': [],
            'left_idle': [],
            'up_attack': [],
            'right_attack': [],
            'down_attack': [],
            'left_attack': [],
        }

        for animation in self.animations.keys():
            animation_path = 'graphics/player/' + animation
            self.animations[animation] = import_images(animation_path)

    def input(self):
        # movement y
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # movement x
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(MAGIC_DATA.keys())[self.magic_index]
                strength = list(MAGIC_DATA.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(MAGIC_DATA.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(WEAPON_DATA.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(MAGIC_DATA.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(MAGIC_DATA.keys())[self.magic_index]

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        # attack status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if not 'attack' in self.status:
                if not 'idle' in self.status:
                    self.status = self.status + '_attack'
                else:
                    self.status = self.status.replace('_idle', '_attack')
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def get_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = WEAPON_DATA[self.weapon]['damage']

        return base_damage + weapon_damage

    def get_magic_damage(self):
        base_damage = self.stats['magic']
        magic_damage = MAGIC_DATA[self.magic]['strength']

        return base_damage + magic_damage

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def timers(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + WEAPON_DATA[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hit_area.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.timers()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
