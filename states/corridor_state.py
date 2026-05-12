import pygame
from core.game_state import State
from core.settings import *
from core.resources import ResourceManager
from ui.button import Button

class CorridorState(State):
    def __init__(self, player, state_manager):
        super().__init__()
        self.player = player
        self.state_manager = state_manager

        self.bg = ResourceManager.get_image("corridor_bg")
        self.font = ResourceManager.get_font("large")

        # Кнопки
        btn_w, btn_h = 200, 60
        center_x = SCREEN_WIDTH // 2 - btn_w // 2
        self.button_cabinet = Button(
            pygame.Rect(center_x, 300, btn_w, btn_h),
            "В кабинет",
            self.go_to_cabinet
        )
        self.button_tutor = Button(
            pygame.Rect(center_x, 400, btn_w, btn_h),
            "Тьюторская",
            self.go_to_tutor
        )

    def go_to_cabinet(self):
        self.state_manager.change_state("cabinet")

    def go_to_tutor(self):
        self.state_manager.change_state("tutor")

    def handle_events(self, events):
        for event in events:
            self.button_cabinet.handle_event(event)
            self.button_tutor.handle_event(event)

    def update(self, dt):
        self.player.update_energy(dt)
        self.button_cabinet.update(dt)
        self.button_tutor.update(dt)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        # Заголовок
        title = self.font.render("Коридор", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title, title_rect)

        self.button_cabinet.draw(screen)
        self.button_tutor.draw(screen)

        # Информация о ресурсах (кратко)
        info_font = ResourceManager.get_font("small")
        info_text = f"Жетоны: {self.player.total_tokens}  Энергия: {int(self.player.energy)}"
        info_surf = info_font.render(info_text, True, WHITE)
        screen.blit(info_surf, (20, SCREEN_HEIGHT - 40))