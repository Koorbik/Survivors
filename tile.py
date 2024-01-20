import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    """
    The Tile class represents a tile in the game. It is a subclass of pygame.sprite.Sprite.
    It has a sprite type and an image, and it belongs to certain groups.

    :param pos: The initial position of the tile.
    :param groups: The groups that the tile belongs to.
    :param sprite_type: The type of the sprite.
    :param surface: The surface of the tile. By default, it is a new surface with the size of a tile.
    """

    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        """
        This method initializes a Tile object. It calls the superclass' __init__ method and sets up the sprite type,
        image, rect, and hitbox.

        :param pos: The initial position of the tile.
        :param groups: The groups that the tile belongs to.
        :param sprite_type: The type of the sprite.
        :param surface: The surface of the tile. By default, it is a new surface with the size of a tile.
        """
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
