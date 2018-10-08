import pygame
from pygame.sprite import Sprite


class Ufo(Sprite):
    image: None

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Ufo, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/Alien_ship.bmp')
        self.image = pygame.transform.scale(self.image, (65, 65))

        self.rect = self.image.get_rect()
        self.rect.x = -10
        self.rect.y = 30

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ufo at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the ufo right or left"""
        self.x += (self.ai_settings.ufo_speed_factor * self.ai_settings.ufo_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if ufo is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
