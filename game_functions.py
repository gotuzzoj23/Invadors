import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from ufo import Ufo
from random import randint
from bunker import Bunker


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, bunkers):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y,
                              bunkers)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, bunkers):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard image
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        bunkers.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        create_bunkers(ai_settings, screen, bunkers)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, clock, ufos, bunkers):
    """Update images on the screen and flip to the new screen"""
    clock.tick(8)
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    ufos.draw(screen)
    aliens.draw(screen)
    bunkers.draw(screen)
    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_bg()
        play_button.draw_button()
        play_button.draw_start_info()


    # Make the most recently drawn screen visible.
    clock.tick(260)
    pygame.display.flip()


def fire_bullet(ai_settings, screen, ship, bullets):
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        bullet_sound()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    """Update position of bullets and get rif of old bullets."""
    # Update bullet position
    bullets.update()
    # Get rid of the bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    # Check for any bullets that have hit aliens.
    # If so, get rif of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            alien_blowup_sound()
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        bunkers.empty()
        ai_settings.increase_speed()
        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
        create_bunkers(ai_settings, screen, bunkers)


def get_number_of_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 1 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_ufo(ai_settings, screen, ufos):
    ufo = Ufo(ai_settings, screen)
    ufo.rect.x = -30
    ufo.rect.y = 30
    ufos.add(ufo)


def update_ufo(ai_settings, screen, stats, sb, ufos, bullets):
    now = pygame.time.get_ticks()
    if len(ufos) <= 0:
        if now - ai_settings.ufo_last > randint(7000, 15000):
            now = pygame.time.get_ticks()
            create_ufo(ai_settings, screen, ufos)
            bunker_move_sound()
    ufos.update()
    for ufo_ship in ufos.sprites():
        if ufo_ship.check_edges():
            ufos.empty()
            ai_settings.ufo_last = now
            break
    check_bullet_ufo_collisions(ai_settings, stats, sb, ufos, bullets)


def create_alien(ai_settings, screen, aliens, alien_number, row_number, index):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1 * (alien.rect.height/2) * row_number
    alien.index = index
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_of_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    index = 0
    for row_number in range(number_rows):
        if row_number < 2:
            index = 0
        elif (row_number > 1) and (row_number < 4):
            index = 2
        elif (row_number > 3) and (row_number < 6):
            index = 4
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number, index)
        ai_settings.alien_index += 1


def create_bunkers(ai_settings, screen, bunkers):
    bunker = Bunker(ai_settings, screen)
    num_of_bunkers = bunker.num_of_bunkers
    for x in range(0, num_of_bunkers):
        create_bunker(ai_settings, screen, bunkers, x)


def create_bunker(ai_settings, screen, bunkers, bunker_num):
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = (bunker_width + 5 * bunker_width * bunker_num) + 20
    bunker.rect.x = bunker.x
    bunker.rect.y = ai_settings.screen_height - 150
    bunkers.add(bunker)


def update_bunkers(bullets, bunkers):
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, True)
    if collisions:
        for _ in collisions.values():
            bunker_blowup_sound()


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens  that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (2 * alien_height) - ship_height)
    number_rows = int(available_space_y / (alien_height * 1.5))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    """Check if fleet is at an edge, and then update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    """Respond to ship being hit by alien."""
    # if you make it equal to 0 it would traverse an extra time and give an extra life
    if stats.ships_left > 1:
        ship_hit_sound()
        # Decrement ships_left.
        stats.ships_left -= 1
        # Update scoreboard.
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        bunkers.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        create_bunkers(ai_settings, screen, bunkers)
        ship.center_ship()
        # Pause
        sleep(0.5)
    else:
        game_over_sound()
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
            break


def check_bullet_ufo_collisions(ai_settings, stats, sb, ufos, bullets):
    # Check for any bullets that have hit aliens.
    # If so, get rif of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, ufos, True, True)
    if collisions:
        for ufo in collisions.values():
            ufo_blowup_sound()   # ufo_blowup_sound
            stats.score += ai_settings.ufo_points * len(ufo)
            sb.prep_score()
            check_high_score(stats, sb)


def check_high_score(stats, sb):
    """Check to see if there's a ner high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def bullet_sound():
    bulletsound = pygame.mixer.Sound("sounds/bullet_sound.ogg")
    bulletsound.set_volume(.5)
    pygame.mixer.Sound.play(bulletsound)


def alien_blowup_sound():
    alien_blow_audio = pygame.mixer.Sound("sounds/alien_blow_sound.ogg")
    alien_blow_audio.set_volume(.5)
    pygame.mixer.Sound.play(alien_blow_audio)


def ship_hit_sound():
    ship_hit_audio = pygame.mixer.Sound("sounds/ship_hit_sound.ogg")
    ship_hit_audio.set_volume(7.0)
    pygame.mixer.Sound.play(ship_hit_audio)


def game_over_sound():
    game_over_audio = pygame.mixer.Sound("sounds/game_over_sound.ogg")
    game_over_audio.set_volume(1.0)
    pygame.mixer.Sound.play(game_over_audio)


def ufo_blowup_sound():
    ufo_hit_audio = pygame.mixer.Sound("sounds/ufo_blowup_sound.ogg")
    ufo_hit_audio.set_volume(1.0)
    pygame.mixer.Sound.play(ufo_hit_audio)


def bunker_blowup_sound():
    bunker_hit_audio = pygame.mixer.Sound("sounds/bunker_hit_sound.ogg")
    bunker_hit_audio.set_volume(1.0)
    pygame.mixer.Sound.play(bunker_hit_audio)


def bunker_move_sound():
    ufo_move_audio = pygame.mixer.Sound("sounds/ufo_move_sound.ogg")
    ufo_move_audio.set_volume(1.0)
    pygame.mixer.Sound.play(ufo_move_audio)
