import pygame
from core.settings import *
from ui.button import Button

class ShopMenu:
    def __init__(self, screen_rect, player, font=None, small_font=None):
        self.screen_rect = screen_rect
        self.player = player
        self.font = font or pygame.font.Font(None, 32)
        self.small_font = small_font or pygame.font.Font(None, 24)

        # Размеры окна
        self.width = 600
        self.height = 400
        self.rect = pygame.Rect(
            (screen_rect.width - self.width) // 2,
            (screen_rect.height - self.height) // 2,
            self.width,
            self.height
        )

        self.active = False
        self.buttons = []          # кнопки покупки и закрытия
        self.upgrade_items = []    # данные об улучшениях для отрисовки

        # Цвета
        self.bg_color = (30, 30, 60, 230)
        self.border_color = WHITE
        self.text_color = WHITE
        self.highlight_color = YELLOW

    def open(self):
        self.active = True
        self._build_buttons()

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

        # Улучшение k (пока одно)
        cost = self.player.upgrade_cost()
        level = self.player.k
        name = "Множитель кликов (k)"
        desc = f"Увеличивает количество жетонов за серию кликов.\nТекущий уровень: {level}\nСтоимость: {cost} жетонов"
        btn_rect = pygame.Rect(self.rect.centerx - 100, self.rect.bottom - 80, 200, 40)
        buy_btn = Button(btn_rect, "Купить", lambda: self._buy_upgrade("k"),
                         font=self.small_font,
                         normal_color=GREEN, hover_color=LIGHT_GRAY, pressed_color=BLUE,
                         text_color=BLACK)
        self.buttons.append(buy_btn)

        self.upgrade_items.append({
            "name": name,
            "desc": desc,
            "button": buy_btn,
            "type": "k"
        })

        # В будущем сюда добавлять другие улучшения

    def _buy_upgrade(self, upgrade_type):
        if upgrade_type == "k":
            if self.player.buy_upgrade():
                # Обновить меню после покупки
                self._build_buttons()
            else:
                # Можно показать временное сообщение "Недостаточно жетонов"
                print("Недостаточно жетонов")  # или добавить всплывающую подсказку

    def handle_event(self, event):
        if not self.active:
            return False

        # Проверяем клик вне окна для закрытия
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.rect.collidepoint(event.pos):
                self.close()
                return True

        for btn in self.buttons:
            btn.handle_event(event)
        return True  # поглощаем события

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

        # Основное окно
        shop_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        shop_surface.fill(self.bg_color)
        pygame.draw.rect(shop_surface, self.border_color, shop_surface.get_rect(), 3)

        # Заголовок
        title = self.font.render("Улучшения", True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 30))
        shop_surface.blit(title, title_rect)

        # Отрисовка улучшений
        y = 80
        for item in self.upgrade_items:
            name_surf = self.small_font.render(item["name"], True, self.highlight_color)
            shop_surface.blit(name_surf, (20, y))
            y += 25

            # Описание может быть многострочным
            for line in item["desc"].split('\n'):
                desc_surf = self.small_font.render(line, True, self.text_color)
                shop_surface.blit(desc_surf, (30, y))
                y += 20
            y += 10

        screen.blit(shop_surface, self.rect.topleft)

        # Кнопки (отрисовываются отдельно, так как они могут выходить за пределы shop_surface? 
        # Лучше рисовать их прямо на screen, пересчитав координаты)
        for btn in self.buttons:
            # Кнопки уже имеют абсолютные координаты относительно экрана
            btn.draw(screen)