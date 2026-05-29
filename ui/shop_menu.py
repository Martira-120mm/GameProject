import pygame
import random
from core.settings import *
from ui.button import Button
from core.resources import ResourceManager


class ShopMenu:
    def __init__(self, screen_rect, player, font=None, small_font=None):
        self.screen_rect = screen_rect
        self.player = player
        self.font = font or pygame.font.Font(None, 32)
        self.small_font = small_font or pygame.font.Font(None, 24)

        # --- Текстура тьютора (чуть ниже) ---
        self.tutor_image = ResourceManager.get_image("tutor")
        if self.tutor_image:
            self.tutor_size = (230, 320)
            self.tutor_image = pygame.transform.scale(self.tutor_image, self.tutor_size)
        else:
            self.tutor_size = (0, 0)

        # Размеры окна магазина
        self.width = 550
        self.height = 300
        self.rect = pygame.Rect(
            (screen_rect.width - self.width) // 2 + self.tutor_size[0] - 150,
            (screen_rect.height - self.height) // 2 - 50,
            self.width,
            self.height
        )

        # --- Диалоговое окно под магазином ---
        self.dialog_height = 100
        self.dialog_rect = pygame.Rect(
            self.rect.x,
            self.rect.bottom + 15,
            self.width,
            self.dialog_height
        )
        self.dialog_text = ""
        self.dialog_speaker = "Тьютор"

        self.active = False
        self.buttons = []
        self.upgrade_items = []

        # Цвета
        self.bg_color = (30, 30, 60, 230)
        self.border_color = WHITE
        self.text_color = WHITE
        self.highlight_color = YELLOW
        self.dialog_bg_color = (20, 20, 40, 220)
        self.dialog_border_color = WHITE
        self.dialog_text_color = WHITE
        self.dialog_name_color = YELLOW

        # Список всех фраз тьютора (для смены по клику)
        self.tutor_phrases = ResourceManager.get_dialog("tutor", "greeting")
        if not self.tutor_phrases or not isinstance(self.tutor_phrases, list):
            self.tutor_phrases = ["Добро пожаловать! Здесь можно улучшить множитель k."]

    def open(self):
        self.active = True
        self._load_random_dialog()
        self._build_buttons()

    def _load_random_dialog(self):
        """Загружает случайную фразу тьютора."""
        self.dialog_text = random.choice(self.tutor_phrases)

    def _next_dialog(self):
        """Меняет текст диалога на другую случайную фразу (не повторяя текущую)."""
        # Получаем список фраз, исключая текущую
        other_phrases = [p for p in self.tutor_phrases if p != self.dialog_text]
        if other_phrases:
            self.dialog_text = random.choice(other_phrases)
        else:
            # Если все фразы одинаковые (маловероятно) – берём любую
            self.dialog_text = random.choice(self.tutor_phrases)

    def close(self):
        self.active = False
        self.buttons.clear()
        self.upgrade_items.clear()

    def _build_buttons(self):
        self.buttons.clear()
        self.upgrade_items.clear()

        # Кнопка закрытия (крестик)
        close_btn = Button(
            pygame.Rect(self.rect.right - 30, self.rect.top + 10, 20, 20),
            "X", self.close,
            font=self.small_font,
            normal_color=RED, hover_color=(255, 100, 100), pressed_color=(200, 0, 0),
            text_color=WHITE
        )
        self.buttons.append(close_btn)

        # Улучшение k (кнопка справа от описания)
        cost = self.player.upgrade_cost()
        level = self.player.k
        name = "Множитель кликов (k)"
        desc_lines = [
            f"Текущий уровень: {level}",
            f"Стоимость: {cost} жетонов"
        ]

        btn_width = 120
        btn_height = 40
        btn_x = self.rect.right - btn_width - 30
        btn_y = self.rect.y + 110
        buy_btn = Button(
            pygame.Rect(btn_x, btn_y, btn_width, btn_height),
            "Купить",
            lambda: self._buy_upgrade("k"),
            font=self.small_font,
            normal_color=GREEN, hover_color=LIGHT_GRAY, pressed_color=BLUE,
            text_color=BLACK
        )
        self.buttons.append(buy_btn)

        self.upgrade_items.append({
            "name": name,
            "desc_lines": desc_lines,
            "button": buy_btn,
            "type": "k"
        })

    def _buy_upgrade(self, upgrade_type):
        if upgrade_type == "k":
            if self.player.buy_upgrade():
                self._build_buttons()
                self._load_random_dialog()   # обновить диалог после покупки
            else:
                # Временное сообщение (без таймера, меняем текст и возвращаем через 2 секунды)
                self._temp_message("Недостаточно жетонов!")

    def _temp_message(self, msg):
        """Показывает временное сообщение, затем возвращает случайную фразу."""
        old_text = self.dialog_text
        self.dialog_text = msg
        # Используем таймер для возврата
        pygame.time.set_timer(pygame.USEREVENT + 1, 2000, True)
        # Сохраняем старый текст, чтобы восстановить
        self._pending_text = old_text

    def handle_event(self, event):
        if not self.active:
            return False

        # Обработка таймера для восстановления текста после "Недостаточно жетонов"
        if event.type == pygame.USEREVENT + 1:
            if hasattr(self, '_pending_text'):
                self.dialog_text = self._pending_text
                del self._pending_text
            else:
                self._load_random_dialog()
            return True

        # Клик по диалоговому окну – меняем текст
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.dialog_rect.collidepoint(event.pos):
                self._next_dialog()
                return True

            # Закрытие магазина по клику вне всех элементов
            if not self.rect.collidepoint(event.pos) and not self.dialog_rect.collidepoint(event.pos):
                # Проверяем также область текстуры тьютора (чтобы не закрывать при клике на него)
                tutor_rect = pygame.Rect(
                    self.rect.left - self.tutor_size[0] + 40,
                    self.rect.centery - self.tutor_size[1] // 2 + 30,   # смещение для нижней позиции
                    *self.tutor_size
                )
                if not tutor_rect.collidepoint(event.pos):
                    self.close()
                    return True

        for btn in self.buttons:
            btn.handle_event(event)
        return True

    def update(self, dt):
        if not self.active:
            return
        for btn in self.buttons:
            btn.update(dt)

    def draw(self, screen):
        if not self.active:
            return

        # Затемнение фона
        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # --- Отрисовка тьютора (сдвинут вниз на 30 пикселей) ---
        if self.tutor_image:
            tutor_x = self.rect.left - self.tutor_size[0] + 40
            tutor_y = self.rect.centery - self.tutor_size[1] // 2 + 50
            screen.blit(self.tutor_image, (tutor_x, tutor_y))

        # --- Окно магазина ---
        shop_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        shop_surface.fill(self.bg_color)
        pygame.draw.rect(shop_surface, self.border_color, shop_surface.get_rect(), 3)

        title = self.font.render("Улучшения", True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 30))
        shop_surface.blit(title, title_rect)

        y = 80
        for item in self.upgrade_items:
            name_surf = self.small_font.render(item["name"], True, self.highlight_color)
            shop_surface.blit(name_surf, (20, y))
            y += 25
            for line in item["desc_lines"]:
                desc_surf = self.small_font.render(line, True, self.text_color)
                shop_surface.blit(desc_surf, (30, y))
                y += 20
            y += 10

        screen.blit(shop_surface, self.rect.topleft)

        # --- Диалоговое окно (кликабельное) ---
        dialog_surface = pygame.Surface((self.width, self.dialog_height), pygame.SRCALPHA)
        dialog_surface.fill(self.dialog_bg_color)
        pygame.draw.rect(dialog_surface, self.dialog_border_color, dialog_surface.get_rect(), 2)

        name_surf = self.small_font.render(self.dialog_speaker, True, self.dialog_name_color)
        dialog_surface.blit(name_surf, (15, 10))

        self._render_text(dialog_surface, self.dialog_text, (15, 45), self.width - 30)

        screen.blit(dialog_surface, self.dialog_rect.topleft)

        # Кнопки (в том числе "Купить" и "X")
        for btn in self.buttons:
            btn.draw(screen)

    def _render_text(self, surface, text, pos, max_width):
        """Перенос текста и отрисовка на surface."""
        font = self.small_font
        words = text.split(' ')
        x, y = pos
        space_width = font.size(' ')[0]
        for word in words:
            word_surf = font.render(word, True, self.dialog_text_color)
            word_width = word_surf.get_width()
            if x + word_width > max_width:
                x = pos[0]
                y += font.get_linesize()
            surface.blit(word_surf, (x, y))
            x += word_width + space_width