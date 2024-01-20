import sys
import pygame
import os
import settings
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from debug import debug
from UI import UI
from enemy import Enemy
from upgrade import Upgrade


class Level:
    """
    The Level class represents a level in the game. It contains methods for creating the map,
    creating attacks, creating enemies, and running the game logic. It also handles player logic,
    checks for player death, and displays game over and win screens.
    """

    def __init__(self):
        """
        This method initializes a Level object. It sets up the display surface, sprite groups,
        UI, upgrades, and sounds. It also calls the create_map method to create the map.
        """

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        # sprites
        self.opposite_attack = None
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.collectable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # UI setup
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        self.upgrade_performed = False

        # sounds
        self.haps = pygame.mixer.Sound('sounds/haps.mp3')
        self.haps.set_volume(0.4)
        self.victory = pygame.mixer.Sound('sounds/victory.mp3')
        self.victory.set_volume(0.4)
        self.gameOver = pygame.mixer.Sound('sounds/gameOver.wav')
        self.gameOver.set_volume(0.4)
        self.player_hit_sound = pygame.mixer.Sound('sounds/player_hit.wav')
        self.player_hit_sound.set_volume(0.3)
        self.background_music = pygame.mixer.Sound('sounds/background_music.wav')
        self.background_music.set_volume(0.1)
        self.background_music.play(loops=-1)

    def create_map(self):
        """
        This method creates the map for the game. It imports the map layout and graphics from CSV files and folders,
        and creates tiles for each element in the map.
        """

        layout = {
            'boundary': import_csv('map/map2_FloorBlocks.csv'),
            'object': import_csv('map/map2_Objects.csv'),
            'food': import_csv('map/map2_Food.csv'),
            'entity': import_csv('map/map2_Entities.csv'),
        }
        graphics = {
            'objects': import_folder('graphics/Objects'),
            'food': import_folder('graphics/Food'),
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'object':
                            surface = graphics['objects'][int(column)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)
                        if style == 'food':
                            random_food_image = choice(graphics['food'])
                            Tile((x, y), [self.visible_sprites, self.collectable_sprites], 'food', random_food_image)
                        if style == 'entity':
                            if column == '394':
                                self.player = Player((x, y), [self.visible_sprites, self.player_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack, self.destroy_weapon)

    def create_attack(self):
        """
        This method creates an attack for the player.
        It creates a Weapon object and assigns it to the current_attack attribute.
        If the level is 3 or higher, it also creates an opposite attack.
        """

        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        if settings.LEVEL >= 3:
            self.opposite_attack = self.current_attack.spawn_opposite_weapon(
                self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_weapon(self):
        """
        This method destroys the current and opposite attacks by calling the kill method on them
        and setting them to None.
        """

        if self.current_attack:
            self.current_attack.kill()

        if self.opposite_attack:
            self.opposite_attack.kill()
        self.current_attack = None
        self.opposite_attack = None

    def create_enemy(self):
        """
        This method creates enemies for the game. It selects a random enemy from the list of enemies
        and creates an Enemy object for it.
        """

        for enemy in settings.enemies:
            enemy_name = enemy
            Enemy(enemy_name, (randint(1100, 2500), randint(600, 2900)),
                  [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player)

    def player_logic(self):
        """
        This method handles the player logic. It checks for collisions between the player's attacks and the enemies,
        and between the player and the collectable items. If a collision is detected, it calls the appropriate methods.
        """

        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)
        if self.collectable_sprites:
            for collectable_sprite in self.collectable_sprites:
                collision_sprites = pygame.sprite.spritecollide(collectable_sprite, self.player_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        self.player.health += 30
                        collectable_sprite.kill()
                        self.haps.play()

    def damage_player(self, amount):
        """
        This method damages the player. It decreases the player's health by the given amount and plays a sound.
        """

        if self.player.vulnerable:
            self.player.health -= amount
            self.player_hit_sound.play()
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def show_game_over(self):
        """
        This method displays the game over screen. It fills the display surface with black, renders the game over text,
        and plays the game over sound. It then waits for 5 seconds before quitting the game.
        """

        game_over_font = pygame.font.Font(None, 100)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(game_over_text, game_over_rect)
        self.background_music.stop()
        self.gameOver.play()
        pygame.display.flip()

        # Wait for 5 seconds
        pygame.time.wait(5000)

        pygame.quit()
        sys.exit()

    def show_win(self):
        """
        This method displays the win screen. It fills the display surface with black, renders the win text,
        and plays the victory sound. It then waits for 5 seconds before quitting the game.
        """

        win_font = pygame.font.Font(UI_FONT, 100)
        win_text = win_font.render("You WON!!!", True, (0, 255, 0))
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(win_text, win_rect)
        self.background_music.stop()
        self.victory.play()
        pygame.display.flip()

        # Wait for 5 seconds
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

    def check_win(self):
        """
        This method checks if the player has won the game. If the level is 10, it calls the show_win method.
        """

        if settings.LEVEL == 10:
            self.show_win()

    def check_death(self):
        """
        This method checks if the player has died. If the player's health is 0 or less,
        it calls the show_game_over method.
        """

        if self.player.health <= 0:
            self.show_game_over()

    def run(self):
        """
        This method runs the game logic. It updates the sprites, checks for player death and win, and draws the UI.
        If the game is not paused, it continues the game logic.
        """

        self.visible_sprites.custom_draw(self.player)
        self.ui.draw(self.player)

        if not self.game_paused:  # Check if the game is not paused
            if not self.player.upgrade_performed:
                self.upgrade.display()
            else:
                # Continue the game logic
                if len(settings.enemies) == 0:
                    settings.LEVEL += 1
                    settings.WAVE_SIZE += 5
                    for i in range(settings.WAVE_SIZE):
                        settings.enemies.append(choice(list(enemy_data.keys())))
                    self.create_enemy()

                    # Reset the upgrade flag in the player
                    self.player.reset_upgrade_flag()

                self.visible_sprites.update()
                self.visible_sprites.enemy_update(self.player)
                self.player_logic()
                self.check_death()
                self.check_win()


class YSortCameraGroup(pygame.sprite.Group):
    """
    The YSortCameraGroup class is a subclass of pygame.sprite.Group. It overrides the draw method to sort the sprites
    by their y-coordinate before drawing them. This creates a depth effect, where sprites with a higher y-coordinate
    (i.e., sprites that are lower on the screen) are drawn on top of sprites with a lower y-coordinate.
    """

    def __init__(self):
        """
        This method initializes a YSortCameraGroup object. It calls the superclass's __init__ method and
        sets up the display surface,
        half width, half height, and offset.
        """

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_rect().centerx
        self.half_height = self.display_surface.get_rect().centery
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surface = pygame.image.load('graphics/map2.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        """
        This method draws the sprites in the group. It first draws the floor,
        then sorts the sprites by their y-coordinate and draws them.
        It also updates the offset based on the player's position.
        """

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        self.display_surface.blit(self.floor_surface, self.floor_rect.topleft - self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        """
        This method updates the enemies in the group.
        It gets the enemy sprites from the group and calls their enemy_update method.
        """

        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                         and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
