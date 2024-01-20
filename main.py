import pygame
import sys
from settings import *
from level import Level
from Button import Button


def main_menu():
    """
    This function is the main menu of the game. It initializes the game, creates the start and exit buttons,
    and waits for the user to press the Enter key to start the game or click the exit button to exit the game.
    """
    run = True
    game = Game()  # Initialize the game
    clock = pygame.time.Clock()  # Initialize the clock
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set the display mode
    start_img = pygame.image.load("start_img.png").convert_alpha()
    exit_img = pygame.image.load("exit_img.png").convert_alpha()
    explanation = pygame.transform.rotozoom(pygame.image.load("explanation.png"), 0, 1)
    title_font = pygame.font.Font(UI_FONT, 100)  # Set the font for the title
    start_button = Button(WIDTH // 2, HEIGHT * (3 / 5), start_img, 0.8)  # Create the start button
    exit_button = Button(WIDTH // 2, HEIGHT * (4 / 5), exit_img, 0.8)  # Create the exit button
    background = pygame.transform.rotozoom(pygame.image.load("SurvivorsBG.png "), 0, 0.5)

    while run:  # Main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user clicks the close button, exit the game
                run = False
        clock.tick(FPS)  # Set the game's FPS
        screen.blit(background, (0, 0))  # Draw the background
        title = title_font.render("SURVIVORS", 1, "white")  # Render the title
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_width() // 2))
        if start_button.draw():  # If the start button is clicked
            screen.blit(explanation, (0, 0))  # Draw the explanation
            pygame.display.flip()
            enter_pressed = False
            while not enter_pressed:  # Wait for the Enter key to be pressed
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # If the Enter key is pressed
                        enter_pressed = True
                        break
            game.run()  # Run the game
            run = False
        if exit_button.draw():  # If the exit button is clicked, exit the game
            run = False
        pygame.display.update()


class Game:
    """
    This class represents the game. It initializes Pygame, sets the display mode, sets the game's title,
    initializes the game's clock, and creates a Level object.
    """

    def __init__(self):
        """
        This method initializes the game. It initializes Pygame, sets the display mode, sets the game's title,
        initializes the game's clock, and creates a Level object.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survivors')  # Set the game's title
        self.clock = pygame.time.Clock()  # Initialize the game's clock
        self.level = Level()  # Create a Level object

    def run(self):
        """
        This method runs the game. It enters a loop that continues until the user clicks the close button.
        In each iteration of the loop, it fills the screen with black, runs the level, updates the display,
        and ticks the clock.
        """
        while True:  # Game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the user clicks the close button, exit the game
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')  # Fill the screen with black
            self.level.run()  # Run the level
            pygame.display.update()  # Update the display
            self.clock.tick(FPS)


if __name__ == "__main__":
    main_menu()
