import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.images = []
        image = pygame.image.load('images/Alien_righty_1.bmp')
        image = pygame.transform.scale(image, (65, 65))
        self.images.append(image)
        image = pygame.image.load('images/Alien_righty_2.bmp')
        image = pygame.transform.scale(image, (65, 65))
        self.images.append(image)
        image = pygame.image.load('images/Alien_greeny_1.bmp')
        image = pygame.transform.scale(image, (65, 65))
        self.images.append(image)
        image = pygame.image.load('images/Alien_greeny_2.bmp')
        image = pygame.transform.scale(image, (65, 65))
        self.images.append(image)
        image = pygame.image.load('images/Alien_purp_1.bmp')
        image = pygame.transform.scale(image, (65, 65))
        self.images.append(image)
        image = pygame.image.load('images/Alien_purp_2.bmp')
        image = pygame.transform.scale(image, (65, 65))
        self.images.append(image)
        image = pygame.image.load('images/Alien_ship.bmp')
        image = pygame.transform.scale(image, (65, 65))
        self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]

        # Start each new alien near the top left of the screen,
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)


    def blitme(self):
        """Draw th alien at its current location"""
        self.screen.blit(self.image, self.rect)


    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        """Move the alien right or left"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        if self.index == 0:
            self.index = 1
        elif self.index == 1:
            self.index = 0
        elif self.index == 2:
            self.index = 3
        elif self.index == 3:
            self.index = 2
        elif self.index == 4:
            self.index = 5
        elif self.index == 5:
            self.index = 4
        self.image = self.images[self.index]
