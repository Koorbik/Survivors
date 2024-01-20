import pygame
from settings import *
from characters import Characters
from support import *


class Enemy(Characters):
    """
    The Enemy class represents an enemy in the game. It is a subclass of Characters.
    It has methods for importing sprites, getting the player's location, getting the enemy's status,
    performing actions, getting damage, checking death, handling cooldowns, and updating the enemy.

    :param enemy_name: The name of the enemy.
    :param pos: The initial position of the enemy.
    :param groups: The groups that the enemy belongs to.
    :param obstacle_sprites: The sprites that represent obstacles.
    :param damage_player: The function to call to damage the player.
    """

    def __init__(self, enemy_name, pos, groups, obstacle_sprites, damage_player):
        """
        This method initializes an Enemy object. It calls the superclass's __init__ method and sets up the sprite type,
        graphics, movement, stats, player interaction, invincibility timer, and sounds.

        :param enemy_name: The name of the enemy.
        :param pos: The initial position of the enemy.
        :param groups: The groups that the enemy belongs to.
        :param obstacle_sprites: The sprites that represent obstacles.
        :param damage_player: The function to call to damage the player.
        """
        super().__init__(groups)
        self.sprite_type = ('enemy')

        # graphics
        self.import_sprites(enemy_name)
        self.status = 'move'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.enemy_name = enemy_name
        enemy_info = enemy_data[self.enemy_name]
        self.health = enemy_info['health']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_timer = 300

        # sounds
        self.death_sound = pygame.mixer.Sound('sounds/death.wav')
        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')
        self.death_sound.set_volume(0.05)
        self.hit_sound.set_volume(0.05)

    def import_sprites(self, name):
        """
        This method imports the sprites for the enemy.
        It sets up the animations dictionary with the paths to the sprite images.

        :param name: The name of the enemy.
        """
        self.animations = {'move': [], 'attack': []}
        main_path = f'graphics/enemies/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_location(self, player):
        """
        This method gets the player's location relative to the enemy.
        It calculates the distance and direction from the enemy to the player.

        :param player: The player object.
        :return: The distance and direction from the enemy to the player.
        """
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def get_status(self, player):
        """
        This method gets the enemy's status.
        If the player is within the enemy's attack radius, the status is set to 'attack'.
        Otherwise, the status is set to 'move'.

        :param player: The player object.
        """
        distance = self.get_player_location(player)[0]

        if distance <= self.attack_radius:
            self.status = 'attack'
        else:
            self.status = 'move'

    def actions(self, player):
        """
        This method performs the enemy's actions based on its status. If the status is 'attack', it damages the player.
        If the status is 'move', it sets the direction towards the player.

        :param player: The player object.
        """
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.status == 'move':
            self.direction = self.get_player_location(player)[1]

    def get_damage(self, player, attack_type):
        """
        This method damages the enemy. If the enemy is vulnerable, it decreases the enemy's health based on
        the attack type and sets the enemy to be invulnerable.

        :param player: The player object.
        :param attack_type: The type of attack ('weapon' or 'projectile').
        """
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_location(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_attack_damage()
            else:
                pass

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        """
        This method checks if the enemy has died. If the enemy's health is 0 or less,
        it removes the enemy from the enemies list, kills the enemy,
        and plays the death sound.
        """
        if self.health <= 0:
            if self.enemy_name in enemies:
                enemies.remove(self.enemy_name)
            self.kill()
            self.death_sound.play()

    def cooldowns(self):
        """
        This method handles the enemy's cooldowns. If the enemy cannot attack, it checks
        if the attack cooldown has passed and allows the enemy to attack.
        If the enemy is not vulnerable, it checks if the invincibility timer has passed and makes the enemy vulnerable.
        """
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_timer:
                self.vulnerable = True

    def hit_reaction(self):
        """
        This method handles the enemy's hit reaction. If the enemy is not vulnerable, it moves the enemy
        in the opposite direction based on its resistance.
        """
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        """
        This method updates the enemy. It handles the hit reaction, moves the enemy, handles cooldowns,
        and checks if the enemy has died.
        """
        self.hit_reaction()
        self.move(self.speed)
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        """
        This method updates the enemy based on the player. It gets the enemy's status, performs the enemy's actions,
        and updates the enemy.

        :param player: The player object.
        """
        self.get_status(player)
        self.actions(player)
