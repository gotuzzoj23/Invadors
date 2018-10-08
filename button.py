from typing import Optional, Any
import pygame.font
from alien import Alien


class Button:
    msg_image_rect: object
    msg_image: Optional[Any]
    title: Optional[Any]
    title_rect: object
    alien1_info: Optional[Any]
    alien1_info_rect: Optional[Any]
    alien2_info: Optional[Any]
    alien2_info_rect: Optional[Any]
    alien3_info: Optional[Any]
    alien3_info_rect: Optional[Any]
    ufo_info: Optional[Any]
    ufo_info_rect: Optional[Any]

    def __init__(self, ai_settings, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()


        self.alien = Alien(ai_settings, screen)
        self.image_rect = self.alien.images[0].get_rect()
        self.image_rect.centerx = self.screen_rect.centerx - 50
        self.image_rect.centery = self.screen_rect.bottom

        # Start screen
        self.bg_width, self.bg_height = ai_settings.screen_width, ai_settings.screen_height
        self.button_color_bg = (255, 255, 255)
        self.text_color_bg = (0, 0, 0)
        self.rect_bg = pygame.Rect(0, 0, self.bg_width, self.bg_height)
        self.rect_bg.center = self.screen_rect.center
        self.font_title = pygame.font.SysFont(None, 250)
        self.font_alien1_points = pygame.font.SysFont(None, 20)
        self.font_alien2_points = pygame.font.SysFont(None, 20)
        self.font_alien3_points = pygame.font.SysFont(None, 20)
        self.font_ufo_points = pygame.font.SysFont(None, 20)


        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - 50

        # The button message and background needs to be prepped only once
        self.prep_msg(msg)
        self.prep_bg()
        self.prep_info()


    # Start button
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


    # Start screen title and background
    def prep_bg(self):
        self.title = self.font_title.render("INVADORS", True, self.text_color_bg, self.button_color_bg)
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.rect_bg.centerx, 200)

    def draw_bg(self):
        self.screen.fill(self.button_color_bg, self.rect_bg)
        self.screen.fill(self.button_color_bg, self.title_rect)
        self.screen.blit(self.title, self.title_rect)


    # Start screen aliens and points values
    def prep_info(self):
        self.alien1_info = self.font_alien1_points.render("--> 50", True, self.text_color_bg, self.button_color_bg)
        self.alien1_info_rect = self.alien1_info.get_rect()
        self.alien1_info_rect.center = (self.rect_bg.centerx + 25, self.screen_rect.bottom - 350)

        self.alien2_info = self.font_alien2_points.render("--> 50", True, self.text_color_bg, self.button_color_bg)
        self.alien2_info_rect = self.alien2_info.get_rect()
        self.alien2_info_rect.center = (self.rect_bg.centerx + 25, self.screen_rect.bottom - 300)

        self.alien3_info = self.font_alien3_points.render("--> 50", True, self.text_color_bg, self.button_color_bg)
        self.alien3_info_rect = self.alien3_info.get_rect()
        self.alien3_info_rect.center = (self.rect_bg.centerx + 25, self.screen_rect.bottom - 250)

        self.ufo_info = self.font_ufo_points.render("--> 300", True, self.text_color_bg, self.button_color_bg)
        self.ufo_info_rect = self.ufo_info.get_rect()
        self.ufo_info_rect.center = (self.rect_bg.centerx + 25, self.screen_rect.bottom - 200)

    def draw_start_info(self):
        self.screen.fill(self.button_color_bg, self.alien1_info_rect)
        self.screen.blit(self.alien1_info, self.alien1_info_rect)
        self.screen.blit(self.alien.images[0], (self.image_rect.centerx, self.image_rect.centery - 385))

        self.screen.fill(self.button_color_bg, self.alien2_info_rect)
        self.screen.blit(self.alien2_info, self.alien2_info_rect)
        self.screen.blit(self.alien.images[2], (self.image_rect.centerx, self.image_rect.centery - 335))

        self.screen.fill(self.button_color_bg, self.alien3_info_rect)
        self.screen.blit(self.alien3_info, self.alien3_info_rect)
        self.screen.blit(self.alien.images[4], (self.image_rect.centerx, self.image_rect.centery - 285))

        self.screen.fill(self.button_color_bg, self.ufo_info_rect)
        self.screen.blit(self.ufo_info, self.ufo_info_rect)
        self.screen.blit(self.alien.images[6], (self.image_rect.centerx, self.image_rect.centery - 235))
