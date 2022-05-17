import pygame
from os import walk


def import_images(path):
    image_surfaces = []

    for _, __, images in walk(path):
        for image in images:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            image_surfaces.append(image_surface)

    return image_surfaces