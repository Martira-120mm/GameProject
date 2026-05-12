import pygame
from core.settings import *
from ui.button import Button

class DialogBox:
    def __init__(self, screen_rect, font=None, small_font=None):
        self.screen_rect = screen_rect
        self.font = font or pygame.font.Font(None, 32)
        self.small_font = small_font or pygame.font.Font(None, 24)

        # Размеры окна диалога
        self.width = screen_rect.width - 100
        self.height = 180
        self.rect = pygame.Rect(
            (screen_rect.width - self.width) // 2,
            screen_rect.height - self.height - 20,
            self.width,
            self.height
        )

        # Состояние
        self.active = False
        self.text = ""
        self.speaker = ""
        self.full_text = ""
        self.char_index = 0
        self.text_speed = 30
        self.time_accum = 0.0
        self.finished = False

        # Кнопки выбора (опционально)
        self.buttons = []
        self.choice_mode = False
        self.choice_result = None  # сохраняем результат выбора

        # Цвета
        self.bg_color = (20, 20, 40, 220)
        self.border_color = WHITE
        self.text_color = WHITE
        self.name_color = YELLOW

    def show_text(self, text, speaker="Преподаватель"):
        """Показать обычный текст (без выбора)."""
        self.active = True
        self.choice_mode = False
        self.speaker = speaker
        self.full_text = text
        self.text = ""
        self.char_index = 0
        self.finished = False
        self.time_accum = 0.0
        self.buttons.clear()

    def show_choice(self, text, speaker, choices, callback):
        """
        Показать диалог с выбором.
        choices: список строк (например, ["Купить", "Отказаться"])
        callback: функция, принимающая индекс выбранного варианта (0 или 1)
        """
        self.active = True
        self.choice_mode = True
        self.speaker = speaker
        self.full_text = text
        self.text = text  # без анимации для простоты, можно оставить
        self.char_index = len(text)
        self.finished = True
        self.time_accum = 0.0
        self.buttons.clear()
        self.choice_callback = callback

        # Создаём кнопки
        btn_width = 150
        btn_height = 40
        spacing = 30
        total_width = len(choices) * btn_width + (len(choices) - 1) * spacing
        start_x = self.rect.x + (self.width - total_width) // 2
        y = self.rect.y + self.height - 60

        for i, label in enumerate(choices):
            btn_rect = pygame.Rect(start_x + i * (btn_width + spacing), y, btn_width, btn_height)
            btn = Button(btn_rect, label, lambda idx=i: self._on_choice(idx),
                         font=self.small_font,
                         normal_color=GRAY, hover_color=LIGHT_GRAY, pressed_color=BLUE,
                         text_color=BLACK)
            self.buttons.append(btn)

    def _on_choice(self, index):
        self.choice_result = index
        self.hide()
        if hasattr(self, 'choice_callback'):
            self.choice_callback(index)

    def hide(self):
        self.active = False
        self.buttons.clear()

    def handle_event(self, event):
        if not self.active:
            return False

        if self.choice_mode:
            for btn in self.buttons:
                btn.handle_event(event)
            return True  # события поглощены

        # Обычный режим текста
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.finished:
                self.hide()
            else:
                self.text = self.full_text
                self.char_index = len(self.full_text)
                self.finished = True
            return True
        return False

    def update(self, dt):
        if not self.active:
            return

        if not self.choice_mode and not self.finished:
            self.time_accum += dt
            chars_to_add = int(self.time_accum * self.text_speed)
            if chars_to_add > 0:
                self.time_accum = 0.0
                self.char_index = min(self.char_index + chars_to_add, len(self.full_text))
                self.text = self.full_text[:self.char_index]
                if self.char_index >= len(self.full_text):
                    self.finished = True

    def draw(self, screen):
        if not self.active:
            return

        # Затемнение фона
        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # Основное окно
        dialog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        dialog_surface.fill(self.bg_color)
        pygame.draw.rect(dialog_surface, self.border_color, dialog_surface.get_rect(), 2)

        # Имя говорящего
        name_surf = self.small_font.render(self.speaker, True, self.name_color)
        dialog_surface.blit(name_surf, (15, 10))

        # Текст
        if self.choice_mode:
            # В режиме выбора текст уже полностью показан
            self._render_text(dialog_surface, self.full_text, (15, 45))
        else:
            self._render_text(dialog_surface, self.text, (15, 45))

        # Индикатор продолжения (если не выбор)
        if not self.choice_mode and self.finished:
            indicator = self.small_font.render("▼", True, WHITE)
            indicator_rect = indicator.get_rect(bottomright=(self.width - 20, self.height - 15))
            dialog_surface.blit(indicator, indicator_rect)

        screen.blit(dialog_surface, self.rect.topleft)

        # Отрисовка кнопок (если есть)
        for btn in self.buttons:
            btn.draw(screen)

    def _render_text(self, surface, text, pos):
        words = text.split(' ')
        x, y = pos
        max_width = self.width - 30
        space_width = self.font.size(' ')[0]
        for word in words:
            word_surf = self.font.render(word, True, self.text_color)
            word_width = word_surf.get_width()
            if x + word_width > max_width:
                x = pos[0]
                y += self.font.get_linesize()
            surface.blit(word_surf, (x, y))
            x += word_width + space_width