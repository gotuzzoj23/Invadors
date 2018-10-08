# Alien Invasion created by Jose Gotuzzo
# Followed directions from  Python Crash Course, by Eric Matthes, and added some new features

import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
from pygame.sprite import Group


def run_game():
    # Initialize Pygame, settings, and screen object.
    pygame.init()
    # Initialize the music game
    clock = pygame.time.Clock()
    pygame.mixer.pre_init(44100, 16, 2, 4096)

    # Settings, start music, and screen object.
    ai_settings = Settings()
    ai_settings.start_music()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Make a ship, group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    # Make a group to store bullets in.
    bullets = Group()
    aliens = Group()
    ufos = Group()
    bunkers = Group()
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop game.

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, bunkers)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
            gf.update_ufo(ai_settings, screen, stats, sb, ufos, bullets)
            gf.update_bunkers(bullets, bunkers)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, clock, ufos, bunkers)


run_game()
