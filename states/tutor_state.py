import pygame
from core.game_state import State
from core.settings import *
from core.resources import ResourceManager
from ui.button import Button
from ui.shop_menu import ShopMenu

class TutorState(State):
    def __init__(self, player, state_manager):
        super().__init__()
        self.player = player
        self.state_manager = state_manager

        self.bg = ResourceManager.get_image("tutor_bg")
        self.font = ResourceManager.get_font("default")
        self.small_font = ResourceManager.get_font("small")

        # Кнопка назад
        self.button_back = Button(
            pygame.Rect(50, 50, 150, 50),
            "← Назад",
            self.go_back,
            font=self.small_font
        )

        # Тьютор
        self.tutor_img = ResourceManager.get_image("tutor")
        self.tutor_rect = pygame.Rect(50, SCREEN_HEIGHT - 350, 120, 200)  # слева

        # Меню магазина
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.shop_menu = ShopMenu(screen_rect, player, font=self.font, small_font=self.small_font)

    def go_back(self):
        self.state_manager.change_state("corridor")

    def handle_events(self, events):
        for event in events:
            if self.shop_menu.active:
                self.shop_menu.handle_event(event)
                continue

            self.button_back.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.tutor_rect.collidepoint(event.pos):
                    self.shop_menu.open()

    def update(self, dt):
        if self.shop_menu.active:
            self.shop_menu.update(dt)
        else:
            self.player.update_energy(dt)
        self.button_back.update(dt)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        # Заголовок
        title = self.font.render("Тьюторская", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title, title_rect)

        # Тьютор слева
        if self.tutor_img:
            screen.blit(self.tutor_img, self.tutor_rect.topleft)
        else:
            # Заглушка
            pygame.draw.rect(screen, (150, 200, 150), self.tutor_rect)

        self.button_back.draw(screen)

        # Информация о ресурсах
        res_text = f"Жетоны: {self.player.total_tokens}   Энергия: {int(self.player.energy)}   Курс: {self.player.course}   k={self.player.k}"
        res_surf = self.small_font.render(res_text, True, WHITE)
        screen.blit(res_surf, (SCREEN_WIDTH//2 - res_surf.get_width()//2, SCREEN_HEIGHT - 50))

        # Меню магазина (поверх всего)
        self.shop_menu.draw(screen)