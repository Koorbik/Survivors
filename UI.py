import pygame
import settings
from settings import *


class UI:
    """
    The UI class represents the user interface in the game.
    It displays the player's health, the current level, and the number of enemies.
    """

    def __init__(self):
        """
        This method initializes a UI object. It gets the display surface, sets the font, and sets up the health bar.
        """
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # health bar setup
        self.health_bar = pygame.Rect(10, 10, BAR_WIDTH, BAR_HEIGHT)

    def show_health(self, current, max_amount, bg_rect, color):
        """
        This method displays the player's health.
        It draws a background rectangle and a foreground rectangle representing the player's current health.

        :param current: The player's current health.
        :param max_amount: The player's maximum health.
        :param bg_rect: The rectangle representing the background of the health bar.
        :param color: The color of the health bar.
        """
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # convert current health to a percentage
        health_percentage = current / max_amount
        current_width = health_percentage * bg_rect.width
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, 'black', bg_rect, 3)

    def show_level(self, level):
        """
        This method displays the current level. It renders the level text and draws it on the display surface.

        :param level: The current level.
        """
        text_surface = self.font.render(f'LEvEL: {level}', False, UI_TEXT_COLOR)
        text_rect = text_surface.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, 'black', text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surface, text_rect)

    def show_enemies(self, enemies):
        """
        This method displays the number of enemies. It renders the enemies text and draws it on the display surface.

        :param enemies: The number of enemies.
        """
        text_surface = self.font.render(f'Enemies: {enemies}', False, UI_TEXT_COLOR)
        text_rect = text_surface.get_rect(bottomleft=(10, HEIGHT - 10))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, 'black', text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surface, text_rect)

    def draw(self, player):
        """
        This method draws the UI. It displays the player's health, the current level, and the number of enemies.

        :param player: The player object.
        """
        self.show_health(player.health, player.stats['health'], self.health_bar, HEALTH_COLOR)
        self.show_level(settings.LEVEL)
        self.show_enemies(len(settings.enemies))
