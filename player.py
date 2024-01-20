import pygame
from settings import *
from support import *
from characters import Characters


class Player(Characters):
    """
    The Player class represents the player character in the game. It is a subclass of Characters.
    It has methods for importing player assets, handling player input, getting the player's status,
    handling player attacks, handling cooldowns, animating the player, getting the player's full attack damage,
    resetting the upgrade flag, and updating the player.
    """

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_weapon):
        """
        This method initializes a Player object. It calls the superclass's __init__ method and sets up the sprite type,
        image, and rect based on the player's status. It also sets up the player's stats, attack properties, and sounds.

        :param pos: The initial position of the player.
        :param groups: The groups that the player belongs to.
        :param obstacle_sprites: The sprites that represent obstacles.
        :param create_attack: The function to call to create an attack.
        :param destroy_weapon: The function to call to destroy a weapon.
        """
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player/right_idle/idle_right.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, -26)

        # graphics
        self.import_player_assets()
        self.status = 'right'

        self.attacking = True
        self.attack_cooldown = 400
        self.attack_duration = 400
        self.attack_time = pygame.time.get_ticks()
        self.reactivation_cooldown = 500
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        # stats
        self.stats = {'health': 150, 'attack': 10, 'speed': 5}
        self.max_stats = {'health': 450, 'attack': 30, 'speed': 10}
        self.health = self.stats['health']
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invincibility_duration = 500

        self.obstacle_sprites = obstacle_sprites
        self.upgrade_performed = False

        # sounds
        self.weapon_attack_sound = pygame.mixer.Sound('sounds/tornadoSound.mp3')
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        """
        This method imports the sprites for the player.
        It sets up the animations dictionary with the paths to the sprite images.
        """
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """
        This method handles player input.
        It checks if the WSAD keys are pressed and sets the player's direction and status accordingly.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def get_status(self):
        """
        This method gets the player's status. If the player is idle, it adds '_idle' to the status.
        If the player is attacking, it adds '_attack' to the status.
        """
        if self.direction == pygame.math.Vector2(0, 0):
            if 'idle' not in self.status and not self.attacking:
                self.status = self.status + '_idle'
        if self.attacking:
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def attack(self):
        """
        This method handles player attacks. If the player can attack, it sets the attack time and creates an attack.
        If the player cannot attack, it checks if the reactivation cooldown has passed and allows the player to attack.
        """
        current_time = pygame.time.get_ticks()

        if not self.attacking and current_time - self.attack_time >= self.reactivation_cooldown + \
                weapon_data[self.weapon]['cooldown']:
            self.attacking = True
            self.attack_time = current_time

        if self.attacking:
            if current_time - self.attack_time > self.attack_duration:
                self.destroy_weapon()
                self.attacking = False
                self.attack_time = current_time
                self.create_attack()
                self.weapon_attack_sound.play()

    def cooldown(self):
        """
        This method handles the player's cooldowns.
        If the player is not vulnerable, it checks if the invincibility duration has passed
        and makes the player vulnerable.
        """
        current_time = pygame.time.get_ticks()
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True

    def animate(self):
        """
        This method animates the player.
        It updates the frame index and sets the player's image to the current frame of the animation.
        """
        animation_list = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation_list):
            self.frame_index = 0

        self.image = animation_list[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def get_full_attack_damage(self):
        """
        This method gets the player's full attack damage. It adds the player's attack stat to the weapon's damage.

        :return: The player's full attack damage.
        """
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_value_by_index(self, index):
        """
        This method gets the value of a player stat by its index.

        :param index: The index of the stat.
        :return: The value of the stat.
        """
        return list(self.stats.values())[index]

    def reset_upgrade_flag(self):
        """
        This method resets the player's upgrade flag. It sets the upgrade_performed attribute to False.
        """
        self.upgrade_performed = False

    def update(self):
        """
        This method updates the player.
        It handles player input, player attacks, cooldowns, player movement, player status, and player animation.
        """
        self.input()
        self.attack()
        self.cooldown()
        self.move(self.speed)
        self.get_status()
        self.animate()
