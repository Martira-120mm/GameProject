import pygame
from core.game_state import State
from core.settings import *
from core.resources import ResourceManager
from ui.button import Button
from ui.shop_menu import ShopMenu
from core.utils import rel_y, rel_x
from core.settings import DebugConfig

class TutorState(State):
    def __init__(self, player, state_manager):
        super().__init__()
        self.player = player
        self.state_manager = state_manager

        self.bg = ResourceManager.get_image("tutor_bg")
        self.font = ResourceManager.get_font("default")
        self.small_font = ResourceManager.get_font("small")

        # Область клика по тьютору (зелёные уголки)
        self.tutor_click_rect = pygame.Rect(SCREEN_WIDTH/2 - SCREEN_WIDTH*0.19, SCREEN_HEIGHT/2 - SCREEN_HEIGHT*0.4, SCREEN_WIDTH/2.7, SCREEN_HEIGHT/1.8)
        self.tutor_hovered = False
        self.tutor_img = ResourceManager.get_image("tutor")   # не используется, но можно оставить

        # Кнопка "Коридор" (прозрачная)
        self.button_back = Button(
            pygame.Rect(rel_x(0), rel_y(320), rel_x(130), rel_y(400)),
            "Коридор",
            self.go_back,
            font=self.small_font,
            alpha=80,
            normal_color=GRAY, hover_color=LIGHT_GRAY, pressed_color=BLUE,
            text_color=BLACK
        )

        # --- МАГАЗИН УЛУЧШЕНИЙ ---
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.shop_menu = ShopMenu(screen_rect, self.player, self.font, self.small_font)

    def go_back(self):
        self.state_manager.change_state("corridor")

    def handle_events(self, events):
    # Если магазин активен — передаём каждое событие по отдельности
        if self.shop_menu.active:
            for event in events:
                self.shop_menu.handle_event(event)
            return

        for event in events:
            self.button_back.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.tutor_click_rect.collidepoint(event.pos):
                    self.shop_menu.open()
            elif event.type == pygame.MOUSEMOTION:
                self.tutor_hovered = self.tutor_click_rect.collidepoint(event.pos)
                if self.tutor_hovered:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self, dt):
        if self.shop_menu.active:
            self.shop_menu.update(dt)
        else:
            self.player.update_energy(dt)
            self.button_back.update(dt)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        # Отрисовка области тьютора (зелёные уголки) только если магазин НЕ активен
        if not self.shop_menu.active and DebugConfig.show_click_areas:
            self._draw_tutor_area(screen)

        # Информационная панель (ресурсы, курс, k)
        res_text = f"Жетоны: {self.player.total_tokens}   Энергия: {int(self.player.energy)}   Курс: {self.player.course}   k={self.player.k}"
        res_surf = self.small_font.render(res_text, True, WHITE)
        screen.blit(res_surf, (SCREEN_WIDTH//2 - res_surf.get_width()//2, SCREEN_HEIGHT - rel_y(50)))

        if not self.shop_menu.active:
            self.button_back.draw(screen)

        # Магазин рисуется поверх всего
        self.shop_menu.draw(screen)

    def _draw_tutor_area(self, screen):
        """Отрисовывает область клика по тьютору с зелёными уголками."""
        rect = self.tutor_click_rect
        if self.tutor_hovered:
            fill_color = (80, 80, 80, 100)
        else:
            fill_color = (30, 30, 30, 100)
        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        overlay.fill(fill_color)
        screen.blit(overlay, rect.topleft)

        color = GREEN
        length = 20
        thick = 4
        # ВЛ
        pygame.draw.line(screen, color, rect.topleft, (rect.left + length, rect.top), thick)
        pygame.draw.line(screen, color, rect.topleft, (rect.left, rect.top + length), thick)
        # ВП
        pygame.draw.line(screen, color, rect.topright, (rect.right - length, rect.top), thick)
        pygame.draw.line(screen, color, rect.topright, (rect.right, rect.top + length), thick)
        # НЛ
        pygame.draw.line(screen, color, rect.bottomleft, (rect.left + length, rect.bottom), thick)
        pygame.draw.line(screen, color, rect.bottomleft, (rect.left, rect.bottom - length), thick)
        # НП
        pygame.draw.line(screen, color, rect.bottomright, (rect.right - length, rect.bottom), thick)
        pygame.draw.line(screen, color, rect.bottomright, (rect.right, rect.bottom - length), thick)