import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):

    def __init__(self, ai_settings, screen):
        super(Bunker, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/Bunker.bmp')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.left + 30
        self.rect.y = self.rect.bottom - 30
        self.num_of_bunkers = self.ai_settings.num_of_bunkers

    def blitme(self):
        """Draw th alien at its current location"""
        self.screen.blit(self.image, self.rect)

