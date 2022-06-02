import pygame
from particles import Particles
from import_images import import_images
from random import choice


class ParticleAnimation:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_images('graphics/particles/flame/frames'),
            'aura': import_images('graphics/particles/aura'),
            'heal': import_images('graphics/particles/heal/frames'),
            # attacks
            'claw': import_images('graphics/particles/claw'),
            'slash': import_images('graphics/particles/slash'),
            'sparkle': import_images('graphics/particles/sparkle'),
            'leaf_attack': import_images('graphics/particles/leaf_attack'),
            'thunder': import_images('graphics/particles/thunder'),
            # enemy deaths
            'squid': import_images('graphics/particles/smoke_orange'),
            'raccoon': import_images('graphics/particles/raccoon'),
            'spirit': import_images('graphics/particles/nova'),
            'bamboo': import_images('graphics/particles/bamboo'),
            # leafs
            'leaf': (
                import_images('graphics/particles/leaf1'),
                import_images('graphics/particles/leaf2'),
                import_images('graphics/particles/leaf3'),
                import_images('graphics/particles/leaf4'),
                import_images('graphics/particles/leaf5'),
                import_images('graphics/particles/leaf6'),
                self.reflect_images(import_images('graphics/particles/leaf1')),
                self.reflect_images(import_images('graphics/particles/leaf2')),
                self.reflect_images(import_images('graphics/particles/leaf3')),
                self.reflect_images(import_images('graphics/particles/leaf4')),
                self.reflect_images(import_images('graphics/particles/leaf5')),
                self.reflect_images(import_images('graphics/particles/leaf6')),
            )
        }

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)

        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        Particles(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        Particles(pos, animation_frames, groups)
