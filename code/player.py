import pygame
from import_images import import_images


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.status = 'down_idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.hit_area = self.rect.inflate(0, -24)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_timeout = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # player assets
        self.import_player_assets()

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

            # magic
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

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
            if current_time - self.attack_time >= self.attack_timeout:
                self.attacking = False

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
