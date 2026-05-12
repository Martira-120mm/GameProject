import pygame
from core.game_state import State
from core.settings import *
from core.resources import ResourceManager

class EndingState(State):
    def __init__(self, player, state_manager):
        super().__init__()
        self.player = player
        self.state_manager = state_manager

        self.font_large = ResourceManager.get_font("large")
        self.font_small = ResourceManager.get_font("small")
        self.fanfare = ResourceManager.get_sound("fanfare")

        self.alpha = 0
        self.fade_in = True
        self.text_lines = []
        self._prepare_text()

    def _prepare_text(self):
        dialogs = ResourceManager.dialogs.get("ending", {})
        title = dialogs.get("title", "Поздравляем!")
        congrats = dialogs.get("congratulations", "Вы получили диплом!")
        credits = dialogs.get("credits", ["Спасибо за игру!"])

        self.text_lines = [title, "", congrats, ""] + credits
        self.text_lines.append("")
        self.text_lines.append("Нажмите любую клавишу для выхода")

    def on_enter(self, **kwargs):
        if self.fanfare:
            self.fanfare.play()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                exit()

    def update(self, dt):
        if self.fade_in:
            self.alpha = min(255, self.alpha + 100 * dt)
            if self.alpha >= 255:
                self.fade_in = False

    def draw(self, screen):
        # Затемнение
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(min(200, self.alpha))
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Текст
        y = SCREEN_HEIGHT // 2 - len(self.text_lines) * 20
        for line in self.text_lines:
            if line == "":
                y += 30
                continue
            if line.startswith("Нажмите"):
                font = self.font_small
            else:
                font = self.font_large if y < SCREEN_HEIGHT//2 else self.font_small
            text_surf = font.render(line, True, WHITE)
            text_surf.set_alpha(self.alpha)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, y))
            screen.blit(text_surf, text_rect)
            y += 40