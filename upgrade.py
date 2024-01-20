import pygame
from settings import *


class Upgrade:
    """
    The Upgrade class represents the upgrade system in the game.
    It displays the player's stats and allows the player to upgrade them.

    :param player: The player object.
    """

    def __init__(self, player):
        """
        This method initializes an Upgrade object.
        It gets the display surface, sets the font, and sets up the upgrade items.

        :param player: The player object.
        """
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 4
        self.create_items()

        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        """
        This method handles player input for the upgrade system.
        It checks if the arrow keys are pressed and updates the selection index accordingly.
        It also checks if the space key is pressed and triggers the selected upgrade.
        """
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

        space_pressed = keys[pygame.K_SPACE]

        if space_pressed and not self.prev_space_pressed:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.item_list[self.selection_index].trigger(self.player)

        self.prev_space_pressed = space_pressed
        self.selection_cooldown()

    def selection_cooldown(self):
        """
        This method handles the selection cooldown.
        If the player cannot move, it checks if the cooldown has passed and allows the player to move.
        """
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        """
        This method creates the upgrade items.
        It calculates the position of each item and creates an Item object for it.
        """
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            # horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2

            # vertical position
            top = self.display_surface.get_size()[1] * 0.1
            # create the box
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        """
        This method displays the upgrade system.
        It handles player input, displays the upgrade items, and handles the selection cooldown.
        """
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            item.display(self.display_surface, self.selection_index, name, value, max_value)


class Item:
    """
    The Item class represents an upgrade item in the game.

    :param left: The left coordinate of the item.
    :param t: The top coordinate of the item.
    :param w: The width of the item.
    :param h: The height of the item.
    :param index: The index of the item.
    :param font: The font to use for the item.
    """

    def __init__(self, left, t, w, h, index, font):
        """
        This method initializes an Item object. It sets up the rect, index, and font.

        :param left: The left coordinate of the item.
        :param t: The top coordinate of the item.
        :param w: The width of the item.
        :param h: The height of the item.
        :param index: The index of the item.
        :param font: The font to use for the item.
        """
        self.rect = pygame.Rect(left, t, w, h)
        self.index = index
        self.font = font

    def display(self, surface, selection_num, name, value, max_value):
        """
        This method displays the item. It draws the item's rectangle and displays the item's name and value.

        :param surface: The surface to draw on.
        :param selection_num: The index of the currently selected item.
        :param name: The name of the item.
        :param value: The current value of the item.
        :param max_value: The maximum value of the item.
        """
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)

    def display_bar(self, surface, value, max_value, selected):
        """
        This method displays the item's value bar.
        It draws a line representing the maximum value and a rectangle representing the current value.

        :param surface: The surface to draw on.
        :param value: The current value of the item.
        :param max_value: The maximum value of the item.
        :param selected: Whether the item is selected.
        """
        # drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        """
        This method triggers the item's upgrade.
        It increases the player's stat and sets the player's upgrade_performed attribute to True.

        :param player: The player object.
        """
        upgrade_atrtibute = list(player.stats.keys())[self.index]
        player.stats[upgrade_atrtibute] *= 1.2
        if player.stats[upgrade_atrtibute] > player.max_stats[upgrade_atrtibute]:
            player.stats[upgrade_atrtibute] = player.max_stats[upgrade_atrtibute]
        player.upgrade_performed = True

    def display_names(self, surface, name, selected):
        """
        This method displays the item's name. It renders the name and draws it on the surface.

        :param surface: The surface to draw on.
        :param name: The name of the item.
        :param selected: Whether the item is selected.
        """
        color = TEXT_COLOR_SELECTED if selected else UI_TEXT_COLOR

        # title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        surface.blit(title_surf, title_rect)
