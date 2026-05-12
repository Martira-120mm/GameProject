import pygame
from core.settings import *

class MessageBox:
    def __init__(self, rect, font=None, max_messages=5,
                 bg_color=WHITE, text_color=BLACK, border_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.font = font if font else pygame.font.Font(None, 24)
        self.max_messages = max_messages
        self.messages = []
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color

    def add_message(self, text):
        self.messages.append(text)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def clear(self):
        self.messages.clear()

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        line_height = self.font.get_linesize()
        y = self.rect.y + 5
        for msg in self.messages:
            text_surf = self.font.render(msg, True, self.text_color)
            screen.blit(text_surf, (self.rect.x + 5, y))
            y += line_height