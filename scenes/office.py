# scenes/office.py — Кабинет: основная сцена с кликером

import pygame
from scenes.base_scene import BaseScene
from ui.button import Button
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BG_OFFICE, COLOR_PANEL, COLOR_PANEL_BORDER,
    COLOR_TEXT_MAIN, COLOR_TEXT_DIM, COLOR_TEXT_GOLD,
    COLOR_BAR_BG, COLOR_BAR_FILL,
    COLOR_BTN_CLICK, COLOR_BTN_CLICK_HVR,
    COLOR_BTN_NORMAL, COLOR_BTN_HOVER,
)


class OfficeScene(BaseScene):
    """
    Кабинет — главная сцена кликера.
    Игрок кликает по большой кнопке, копит серию кликов, получает жетоны.
    """

    def __init__(self, game_state):
        super().__init__(game_state)

        # --- Шрифты ---
        self.font_big    = pygame.font.SysFont("segoeui", 36, bold=True)
        self.font_mid    = pygame.font.SysFont("segoeui", 22)
        self.font_small  = pygame.font.SysFont("segoeui", 17)

        # --- Главная кнопка клика ---
        btn_w, btn_h = 220, 220
        btn_x = SCREEN_WIDTH // 2 - btn_w // 2
        btn_y = SCREEN_HEIGHT // 2 - btn_h // 2 + 20
        self.click_button = Button(
            btn_x, btn_y, btn_w, btn_h,
            "КЛИКНУТЬ",
            color=COLOR_BTN_CLICK,
            hover_color=COLOR_BTN_CLICK_HVR,
            font=self.font_big,
        )

        # --- Кнопка перехода в коридор ---
        self.corridor_btn = Button(
            SCREEN_WIDTH - 180, SCREEN_HEIGHT - 60, 160, 40,
            "→ Коридор",
            font=self.font_small,
        )

        # --- Флаг вспышки при получении награды ---
        self.flash_timer = 0   # сколько кадров показывать вспышку
        self.FLASH_DURATION = 20

    # ------------------------------------------------------------------
    def handle_events(self, events):
        # Клик по главной кнопке
        if self.click_button.is_clicked(events):
            self.state.add_click()
            if self.state.reward_received:
                self.flash_timer = self.FLASH_DURATION  # запускаем вспышку

        # Переход в коридор
        if self.corridor_btn.is_clicked(events):
            return "corridor"

        return None

    # ------------------------------------------------------------------
    def update(self):
        # Уменьшаем таймер вспышки каждый кадр
        if self.flash_timer > 0:
            self.flash_timer -= 1
        return None

    # ------------------------------------------------------------------
    def draw(self, screen):
        # Фон сцены
        screen.fill(COLOR_BG_OFFICE)

        # Вспышка при получении награды (полупрозрачный белый прямоугольник)
        if self.flash_timer > 0:
            alpha = int(180 * (self.flash_timer / self.FLASH_DURATION))
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 180, alpha))
            screen.blit(flash_surf, (0, 0))

        # --- Верхняя панель со статистикой ---
        self._draw_stats_panel(screen)

        # --- Прогресс-бар серии кликов ---
        self._draw_progress_bar(screen)

        # --- Главная кнопка ---
        self.click_button.draw(screen)

        # --- Подпись под кнопкой ---
        hint = self.font_small.render(
            f"Кликов до жетонов: {self.state.clicks_required - self.state.clicks}",
            True, COLOR_TEXT_DIM
        )
        hint_rect = hint.get_rect(
            centerx=SCREEN_WIDTH // 2,
            top=self.click_button.rect.bottom + 12
        )
        screen.blit(hint, hint_rect)

        # --- Заголовок сцены ---
        title = self.font_mid.render("📚  Кабинет", True, COLOR_TEXT_MAIN)
        screen.blit(title, (20, 20))

        # --- Кнопка перехода ---
        self.corridor_btn.draw(screen)

    # ------------------------------------------------------------------
    # Вспомогательные методы отрисовки
    # ------------------------------------------------------------------
    def _draw_stats_panel(self, screen):
        """Панель с жетонами, курсом и множителем в правом верхнем углу."""
        panel = pygame.Rect(SCREEN_WIDTH - 230, 10, 220, 110)
        pygame.draw.rect(screen, COLOR_PANEL, panel, border_radius=10)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, panel, width=1, border_radius=10)

        lines = [
            (f"🪙 Жетоны:  {self.state.tokens}", COLOR_TEXT_GOLD),
            (f"📖 Курс:     {self.state.course}", COLOR_TEXT_MAIN),
            (f"✖ Множитель: {self.state.k}",      COLOR_TEXT_MAIN),
        ]
        for i, (text, color) in enumerate(lines):
            surf = self.font_small.render(text, True, color)
            screen.blit(surf, (panel.x + 12, panel.y + 12 + i * 30))

    def _draw_progress_bar(self, screen):
        """Прогресс-бар под панелью статистики."""
        bar_x = SCREEN_WIDTH - 230
        bar_y = 130
        bar_w = 220
        bar_h = 18

        # Фон бара
        bg_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
        pygame.draw.rect(screen, COLOR_BAR_BG, bg_rect, border_radius=6)

        # Заполненная часть
        fill_w = int(bar_w * self.state.click_progress)
        if fill_w > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_w, bar_h)
            pygame.draw.rect(screen, COLOR_BAR_FILL, fill_rect, border_radius=6)

        # Текст внутри бара
        label = self.font_small.render(
            f"{self.state.clicks} / {self.state.clicks_required}",
            True, COLOR_TEXT_MAIN
        )
        label_rect = label.get_rect(center=bg_rect.center)
        screen.blit(label, label_rect)
