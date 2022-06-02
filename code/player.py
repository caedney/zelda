import pygame
from settings import *
from import_images import import_images


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)

        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.status = 'down_idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.hit_area = self.rect.inflate(0, -24)
        self.direction = pygame.math.Vector2()
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
        # self.destroy_magic= destroy_magic
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

    def timers(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hit_area.center)

    def update(self):
        self.input()
        self.timers()
        self.get_status()
        self.animate()
        self.move(self.speed)
