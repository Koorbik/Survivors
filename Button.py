import pygame


class Button:
    """
    The Button class represents a clickable button in the game.
    It has methods for drawing the button and checking if it has been clicked.
    """

    def __init__(self, x, y, image, scale):
        """
        This method initializes a Button object.
        It scales the image to the given scale and sets the button's rect to be centered at the given coordinates.
        It also sets the clicked attribute to False and gets the display surface.

        :param x: The x-coordinate of the center of the button.
        :param y: The y-coordinate of the center of the button.
        :param image: The image to be used for the button.
        :param scale: The scale to which the image should be resized.
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale),
                                                    int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.screen = pygame.display.get_surface()

    def draw(self):
        """
        This method draws the button on the screen and checks if it has been clicked.
        :return: True if the button is clicked, False otherwise.
        """
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked is False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
