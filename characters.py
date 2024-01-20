import pygame


class Characters(pygame.sprite.Sprite):
    """
    The Characters class represents a character in the game. It is a subclass of pygame.sprite.Sprite.
    It has methods for moving the character and handling collisions.
    """

    def __init__(self, groups):
        """
        This method initializes a Characters object. It calls the superclass's __init__ method
        and sets up the frame index, animation speed, and direction.

        :param groups: The groups that the character belongs to.
        """
        super().__init__(groups)
        self.frame_index = 0  # The index of the current frame in the animation
        self.animation_speed = 0.15  # The speed of the animation
        self.direction = pygame.math.Vector2()  # The direction of movement

    def move(self, speed):
        """
        This method moves the character. It normalizes the direction vector
        and then moves the character's hitbox in the direction.
        It also handles horizontal and vertical collisions.

        :param speed: The speed of the character's movement.
        """
        if self.direction.magnitude() != 0:  # If the direction vector is not zero
            self.direction = self.direction.normalize()  # Normalize the direction vector

        self.hitbox.x += self.direction.x * speed  # Move the hitbox horizontally
        self.collision('horizontal')  # Handle horizontal collisions
        self.hitbox.y += self.direction.y * speed  # Move the hitbox vertically
        self.collision('vertical')  # Handle vertical collisions
        self.rect.center = self.hitbox.center  # Update the character's position based on the hitbox

    def collision(self, direction):
        """
        This method handles collisions. It checks if the character's hitbox collides with any of the obstacle sprites.
        If a collision is detected, it adjusts the character's position to prevent it from moving into the obstacle.

        :param direction: The direction of movement ('horizontal' or 'vertical').
        """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # If moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # If moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # If moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # If moving up
                        self.hitbox.top = sprite.hitbox.bottom
