import pygame
from upgrade_item import UpgradeItem
from settings import *


class Upgrade:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attr_number = len(player.stats)
        self.attr_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # item creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attr_number)):
            # horizontal pos
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attr_number
            left = (item * increment) + (increment - self.width) // 2

            # vertical pos
            top = self.display_surface.get_size()[1] * 0.1

            # create object
            item = UpgradeItem(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attr_number - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def timers(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()

            if current_time - self.selection_time >= 300:
                self.can_move = True

    def display(self):
        self.input()
        self.timers()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attr_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)
