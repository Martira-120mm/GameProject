# scenes/corridor.py — Коридор: хаб для перехода между сценами

import pygame
from scenes.base_scene import BaseScene
from ui.button import Button
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BG_CORRIDOR, COLOR_PANEL, COLOR_PANEL_BORDER,
    COLOR_TEXT_MAIN, COLOR_TEXT_DIM, COLOR_TEXT_GOLD,
    COLOR_BTN_NORMAL, COLOR_BTN_HOVER,
)


class CorridorScene(BaseScene):
    """
    Коридор — промежуточная сцена-хаб.
    Отображает краткую статистику и кнопки перехода в другие локации.
    """

    def __init__(self, game_state):
        super().__init__(game_state)

        # --- Шрифты ---
        self.font_big   = pygame.font.SysFont("segoeui", 30, bold=True)
        self.font_mid   = pygame.font.SysFont("segoeui", 22)
        self.font_small = pygame.font.SysFont("segoeui", 17)

        # --- Кнопки перехода ---
        btn_w, btn_h = 260, 70
        center_x = SCREEN_WIDTH // 2 - btn_w // 2

        self.office_btn = Button(
            center_x, 260, btn_w, btn_h,
            "📚  Кабинет",
            font=self.font_mid,
        )
        self.tutor_btn = Button(
            center_x, 360, btn_w, btn_h,
            "🎓  Тьюторская",
            font=self.font_mid,
        )

    # ------------------------------------------------------------------
    def handle_events(self, events):
        if self.office_btn.is_clicked(events):
            return "office"
        if self.tutor_btn.is_clicked(events):
            return "tutor_room"
        return None

    # ------------------------------------------------------------------
    def update(self):
        return None

    # ------------------------------------------------------------------
    def draw(self, screen):
        screen.fill(COLOR_BG_CORRIDOR)

        # Заголовок
        title = self.font_big.render("🚪  Коридор", True, COLOR_TEXT_MAIN)
        screen.blit(title, title.get_rect(centerx=SCREEN_WIDTH // 2, top=40))

        subtitle = self.font_small.render(
            "Выберите, куда пойти", True, COLOR_TEXT_DIM
        )
        screen.blit(subtitle, subtitle.get_rect(centerx=SCREEN_WIDTH // 2, top=85))

        # --- Панель статистики ---
        self._draw_stats(screen)

        # --- Кнопки ---
        self.office_btn.draw(screen)
        self.tutor_btn.draw(screen)

        # --- Декоративные подписи рядом с кнопками ---
        self._draw_location_hints(screen)

    # ------------------------------------------------------------------
    def _draw_stats(self, screen):
        """Мини-статистика в центре."""
        panel = pygame.Rect(SCREEN_WIDTH // 2 - 150, 110, 300, 120)
        pygame.draw.rect(screen, COLOR_PANEL, panel, border_radius=12)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, panel, width=1, border_radius=12)

        stats = [
            (f"🪙  Жетоны:    {self.state.tokens}",   COLOR_TEXT_GOLD),
            (f"📖  Курс:       {self.state.course}",   COLOR_TEXT_MAIN),
            (f"✖  Множитель:  {self.state.k}",         COLOR_TEXT_MAIN),
            (f"👆  Кликов:    {self.state.clicks} / {self.state.clicks_required}", COLOR_TEXT_DIM),
        ]
        for i, (text, color) in enumerate(stats):
            surf = self.font_small.render(text, True, color)
            screen.blit(surf, (panel.x + 20, panel.y + 14 + i * 24))

    def _draw_location_hints(self, screen):
        """Небольшие подсказки справа от каждой кнопки."""
        hints = [
            (self.office_btn.rect,  "Зарабатывай жетоны кликами"),
            (self.tutor_btn.rect,   "Трать жетоны на улучшения"),
        ]
        for btn_rect, hint_text in hints:
            hint = self.font_small.render(hint_text, True, COLOR_TEXT_DIM)
            screen.blit(hint, (btn_rect.right + 16, btn_rect.centery - hint.get_height() // 2))
