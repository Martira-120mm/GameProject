# scenes/tutor_room.py — Тьюторская: магазин улучшений

import pygame
from scenes.base_scene import BaseScene
from ui.button import Button
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BG_TUTOR, COLOR_PANEL, COLOR_PANEL_BORDER,
    COLOR_TEXT_MAIN, COLOR_TEXT_DIM, COLOR_TEXT_GOLD, COLOR_TEXT_RED,
    COLOR_BTN_GREEN, COLOR_BTN_GREEN_HVR,
    COLOR_BTN_NORMAL, COLOR_BTN_HOVER,
)


class TutorRoomScene(BaseScene):
    """
    Тьюторская — здесь игрок тратит жетоны на улучшение множителя k.
    Также позволяет сменить курс (1–4), что влияет на порог кликов.
    """

    def __init__(self, game_state):
        super().__init__(game_state)

        # --- Шрифты ---
        self.font_big   = pygame.font.SysFont("segoeui", 28, bold=True)
        self.font_mid   = pygame.font.SysFont("segoeui", 22)
        self.font_small = pygame.font.SysFont("segoeui", 17)

        # --- Кнопка покупки апгрейда ---
        self.upgrade_btn = Button(
            SCREEN_WIDTH // 2 - 150, 280, 300, 60,
            "Купить апгрейд",
            color=COLOR_BTN_GREEN,
            hover_color=COLOR_BTN_GREEN_HVR,
            font=self.font_mid,
        )

        # --- Кнопки выбора курса ---
        self.course_buttons = []
        for i, course in enumerate([1, 2, 3, 4]):
            btn = Button(
                100 + i * 150, 420, 120, 44,
                f"Курс {course}",
                font=self.font_small,
            )
            self.course_buttons.append((course, btn))

        # --- Кнопка назад в коридор ---
        self.back_btn = Button(
            20, SCREEN_HEIGHT - 60, 160, 40,
            "← Коридор",
            font=self.font_small,
        )

        # --- Сообщение обратной связи (например "Недостаточно жетонов") ---
        self.feedback_text  = ""
        self.feedback_timer = 0
        self.FEEDBACK_DURATION = 90  # кадров (~1.5 сек при 60 FPS)

    # ------------------------------------------------------------------
    def handle_events(self, events):
        # Попытка купить апгрейд
        if self.upgrade_btn.is_clicked(events):
            success = self.state.buy_upgrade()
            if success:
                self._show_feedback(
                    f"✅  Улучшение куплено! k = {self.state.k}", ok=True
                )
            else:
                self._show_feedback(
                    f"❌  Нужно {self.state.upgrade_price} жетонов", ok=False
                )

        # Смена курса
        for course, btn in self.course_buttons:
            if btn.is_clicked(events):
                self.state.set_course(course)
                self._show_feedback(f"📖  Курс изменён на {course}", ok=True)

        # Назад в коридор
        if self.back_btn.is_clicked(events):
            return "corridor"

        return None

    # ------------------------------------------------------------------
    def update(self):
        # Отключаем кнопку апгрейда, если жетонов не хватает
        self.upgrade_btn.enabled = self.state.can_upgrade()

        # Уменьшаем таймер сообщения
        if self.feedback_timer > 0:
            self.feedback_timer -= 1

        return None

    # ------------------------------------------------------------------
    def draw(self, screen):
        screen.fill(COLOR_BG_TUTOR)

        # Заголовок
        title = self.font_big.render("🎓  Тьюторская", True, COLOR_TEXT_MAIN)
        screen.blit(title, (20, 20))

        # --- Панель текущего состояния ---
        self._draw_state_panel(screen)

        # --- Карточка апгрейда ---
        self._draw_upgrade_card(screen)

        # Кнопка покупки
        self.upgrade_btn.draw(screen)

        # --- Раздел смены курса ---
        self._draw_course_section(screen)

        # --- Сообщение обратной связи ---
        if self.feedback_timer > 0:
            self._draw_feedback(screen)

        # Кнопка назад
        self.back_btn.draw(screen)

    # ------------------------------------------------------------------
    # Вспомогательные методы
    # ------------------------------------------------------------------
    def _draw_state_panel(self, screen):
        panel = pygame.Rect(SCREEN_WIDTH - 240, 10, 220, 80)
        pygame.draw.rect(screen, COLOR_PANEL, panel, border_radius=10)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, panel, width=1, border_radius=10)

        lines = [
            (f"🪙 Жетоны:  {self.state.tokens}", COLOR_TEXT_GOLD),
            (f"✖ Множитель k = {self.state.k}",  COLOR_TEXT_MAIN),
        ]
        for i, (text, color) in enumerate(lines):
            surf = self.font_small.render(text, True, color)
            screen.blit(surf, (panel.x + 12, panel.y + 12 + i * 28))

    def _draw_upgrade_card(self, screen):
        """Блок с описанием апгрейда перед кнопкой покупки."""
        card = pygame.Rect(SCREEN_WIDTH // 2 - 200, 160, 400, 110)
        pygame.draw.rect(screen, COLOR_PANEL, card, border_radius=12)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, card, width=1, border_radius=12)

        header = self.font_mid.render("Улучшение множителя", True, COLOR_TEXT_MAIN)
        screen.blit(header, header.get_rect(centerx=card.centerx, top=card.top + 14))

        desc = self.font_small.render(
            f"k:  {self.state.k}  →  {self.state.k + 1}   (жетонов за серию кликов)",
            True, COLOR_TEXT_DIM
        )
        screen.blit(desc, desc.get_rect(centerx=card.centerx, top=card.top + 48))

        price_color = COLOR_TEXT_GOLD if self.state.can_upgrade() else COLOR_TEXT_RED
        price = self.font_mid.render(
            f"Цена: {self.state.upgrade_price} 🪙",
            True, price_color
        )
        screen.blit(price, price.get_rect(centerx=card.centerx, top=card.top + 76))

    def _draw_course_section(self, screen):
        """Метки и кнопки выбора курса."""
        label = self.font_mid.render("Выбрать курс:", True, COLOR_TEXT_DIM)
        screen.blit(label, (100, 390))

        for course, btn in self.course_buttons:
            # Подсвечиваем активный курс рамкой
            if course == self.state.course:
                glow = btn.rect.inflate(4, 4)
                pygame.draw.rect(screen, COLOR_TEXT_GOLD, glow, width=2, border_radius=10)
            btn.draw(screen)

        # Подсказка под кнопками
        hint_text = {
            1: "Порог: 20 кликов",
            2: "Порог: 30 кликов",
            3: "Порог: 40 кликов",
            4: "Порог: 20 кликов",
        }
        hint = self.font_small.render(
            hint_text[self.state.course],
            True, COLOR_TEXT_DIM
        )
        screen.blit(hint, (100, 472))

    def _draw_feedback(self, screen):
        """Небольшое сообщение внизу по центру."""
        color = COLOR_TEXT_GOLD if self._feedback_ok else COLOR_TEXT_RED
        surf = self.font_mid.render(self.feedback_text, True, color)
        rect = surf.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 20)

        # Фон под текстом
        bg = rect.inflate(20, 10)
        pygame.draw.rect(screen, COLOR_PANEL, bg, border_radius=8)
        screen.blit(surf, rect)

    def _show_feedback(self, text: str, ok: bool = True):
        self.feedback_text  = text
        self.feedback_timer = self.FEEDBACK_DURATION
        self._feedback_ok   = ok
