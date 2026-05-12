import pygame
from core.settings import *

class Button:
    def __init__(self, rect, text, callback, font=None,
                 normal_color=GRAY, hover_color=LIGHT_GRAY, pressed_color=BLUE,
                 text_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font if font else pygame.font.Font(None, 32)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.text_color = text_color

        self.is_hovered = False
        self.is_pressed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.callback()
            self.is_pressed = False

    def update(self, dt):
        pass

    def draw(self, screen):
        color = self.normal_color
        if self.is_pressed:
            color = self.pressed_color
        elif self.is_hovered:
            color = self.hover_color

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)