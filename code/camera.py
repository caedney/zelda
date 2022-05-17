import pygame


class Camera(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.centerx = self.display_surface.get_size()[0] // 2
        self.centery = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.centerx
        self.offset.y = player.rect.centery - self.centery

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)