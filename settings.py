import pygame


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1000
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship's settings
        self.ship_speed_factor = .5  # 100
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 15  # 50
        self.bullet_width = 10  # 500
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10

        # Alien settings
        self.alien_index = 0
        self.alien_speed_factor = 1   # 30
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # UFO settings
        self.ufo_speed_factor = 4
        self.ufo_direction = 1
        self.ufo_last = 0

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Bunkers
        self.num_of_bunkers = 4

        self.initialize_dynamic_settings()
        self.alien_points = 0
        self.ufo_points = 0


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughput the game."""
        self.ship_speed_factor = 50   # 50
        self.bullet_speed_factor = 25     # 10
        self.alien_speed_factor = 1     # 10
        self.ufo_speed_factor = 13
        # Fleet direction of 1 represents right ; -1 represents left.
        self.fleet_direction = 10
        # Scoring
        self.alien_points = 50
        self.ufo_points = 300

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor += self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.ufo_points = int(self.ufo_points * self.score_scale)
        self.ufo_speed_factor += 1
        # print(self.alien_points)


    def start_music(self):
        pygame.mixer.music.load("sounds/Mozart_Omni.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

