import pygame


class Weapon(pygame.sprite.Sprite):
    """
    The Weapon class represents a weapon in the game. It is a subclass of pygame.sprite.Sprite.
    It has methods for spawning an opposite weapon.

    :param player: The player object.
    :param groups: The groups that the weapon belongs to.
    """

    def __init__(self, player, groups):
        """
        This method initializes a Weapon object. It calls the superclass' __init__ method and sets up the sprite type,
        image, and rect based on the player's status.

        :param player: The player object.
        :param groups: The groups that the weapon belongs to.
        """
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))

    def spawn_opposite_weapon(self, player, groups):
        """
        This method spawns an opposite weapon. It creates a copy of the weapon with a mirrored direction,
        flips the image horizontally, and updates the rect position based on the mirrored direction.

        :param player: The player object.
        :param groups: The groups that the weapon belongs to.
        :return: The opposite weapon.
        """
        # Create a copy of the weapon with a mirrored direction
        opposite_weapon = Weapon(player, groups)

        # Flip the image horizontally
        opposite_weapon.image = pygame.transform.flip(self.image, True, False)

        # Update the rect position based on the mirrored direction
        opposite_weapon.rect = self.rect.copy()

        if player.status.startswith('right'):
            opposite_weapon.rect.midright = player.rect.midleft - pygame.math.Vector2(0, 16)
        elif player.status.startswith('left'):
            opposite_weapon.rect.midleft = player.rect.midright + pygame.math.Vector2(0, 16)
        elif player.status.startswith('up'):
            opposite_weapon.rect.midtop = player.rect.midbottom - pygame.math.Vector2(-10, 0)
        elif player.status.startswith('down'):
            opposite_weapon.rect.midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0)

        return opposite_weapon
