import pygame
from core.settings import *

class ProgressBar:
    def __init__(self, rect, max_value, fill_color=GREEN, bg_color=GRAY, border_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.max_value = max_value
        self.current_value = 0
        self.fill_color = fill_color
        self.bg_color = bg_color
        self.border_color = border_color

    def set_values(self, current, max_val):
        self.current_value = current
        self.max_value = max_val

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        if self.max_value > 0:
            fill_width = int(self.rect.width * (self.current_value / self.max_value))
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, self.fill_color, fill_rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        # Текст прогресса
        font = pygame.font.Font(None, 24)
        text = f"{self.current_value}/{self.max_value}"
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)