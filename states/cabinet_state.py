import pygame
import random
from core.game_state import State
from core.settings import *
from core.resources import ResourceManager
from core.save_load import save_game
from ui.button import Button
from ui.progress_bar import ProgressBar
from entities.player import Player
from entities.progression import Progression
from ui.dialog_box import DialogBox

class CabinetState(State):
    def __init__(self, player, state_manager):

        super().__init__()
        self.player = player
        self.state_manager = state_manager

        # Ресурсы
        self.bg = ResourceManager.get_image("cabinet_bg")
        self.notebook_img = ResourceManager.get_image("notebook")
        self.token_icon = ResourceManager.get_image("token_icon")
        self.energy_icon = ResourceManager.get_image("energy_icon")
        self.font = ResourceManager.get_font("default")
        self.small_font = ResourceManager.get_font("small")

        # Область клика (тетрадь)
        self.click_area = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 140, 200, 280)

        self.teacher_rect = pygame.Rect(50, SCREEN_HEIGHT - 350, 120, 200)
        self.teacher_img = ResourceManager.get_image("teacher")

        # Прогресс-бар
        bar_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 100, 300, 30)
        self.progress_bar = ProgressBar(bar_rect, 1)

        # Кнопка в коридор
        btn_rect = pygame.Rect(SCREEN_WIDTH - 170, 400, 150, 220)
        self.button_corridor = Button(btn_rect, "Коридор", self.go_to_corridor)

        # Звуки
        self.click_sound = ResourceManager.get_sound("click")
        self.token_sound = ResourceManager.get_sound("token")
        self.fanfare_sound = ResourceManager.get_sound("fanfare")

        # Автосохранение
        self.clicks_since_autosave = 0

        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dialog_box = DialogBox(screen_rect)



    def go_to_corridor(self):
        self.state_manager.change_state("corridor")

    def _show_teacher_dialog(self):
        phrases = ResourceManager.get_dialog("teacher", "idle")
        if phrases:
            text = random.choice(phrases)
        else:
            text = "Пишите, студент! Каждый клик приближает вас к диплому."
        self.dialog_box.show(text, speaker="Преподаватель")

    def handle_events(self, events):
        for event in events:
            self.button_corridor.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.dialog_box.active:
                    # Если диалог активен, передаём событие ему
                    self.dialog_box.handle_event(event)
                else:
                    if self.teacher_rect.collidepoint(event.pos):
                        self._show_teacher_dialog()
                    elif self.click_area.collidepoint(event.pos):
                        self._handle_click()
                    elif event.type == pygame.MOUSEMOTION:
                        if self.click_area.collidepoint(event.pos) or self.teacher_rect.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def _handle_teacher_click(self):
        phrases = ResourceManager.get_dialog("teacher", "idle")
        if phrases:
            msg = random.choice(phrases)
        else:
            msg = "Учитель смотрит на вас с укором."


    def _handle_click(self):

        token_earned = self.player.perform_click()
        # Звук клика (заглушка)
        if self.click_sound:
            self.click_sound.play()

        if token_earned:
            # Звук жетона
            if self.token_sound:
                self.token_sound.play()

            # Проверка перехода на курс (произошло внутри perform_click через _grant_token)
            # Проверим, не завершена ли игра
            if self.player.is_game_finished():
                # Воспроизвести фанфары
                if self.fanfare_sound:
                    self.fanfare_sound.play()
                self.state_manager.change_state("ending")
                return

        self._update_progress_bar()

        # Автосохранение
        self.clicks_since_autosave += 1
        if self.clicks_since_autosave >= AUTOSAVE_CLICKS_INTERVAL:
            save_game(self.player.to_dict(), SAVE_FILE_PATH)
            self.clicks_since_autosave = 0

    def _update_progress_bar(self):
        total_needed = Progression.calc_clicks_for_token(self.player.k, self.player.n)
        done = total_needed - self.player.clicks_until_token
        self.progress_bar.set_values(done, total_needed)

    def update(self, dt):
        if self.dialog_box.active:
            self.dialog_box.update(dt)
            # Не обновляем энергию и кнопки, пока диалог активен
            return
        self.player.update_energy(dt)
        self.button_corridor.update(dt)

    def draw(self, screen):

        screen.blit(self.bg, (0, 0))

        # Рисуем тетрадь
        screen.blit(self.notebook_img, self.click_area.topleft)

        # Верхняя панель ресурсов
        self._draw_resource_panel(screen)

        # Прогресс-бар
        self.progress_bar.draw(screen)

        # Кнопка коридора
        self.button_corridor.draw(screen)

        if self.teacher_img:
            screen.blit(self.teacher_img, self.teacher_rect.topleft)
        self.dialog_box.draw(screen)

    def _draw_resource_panel(self, screen):
        # Фон панели
        panel_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        pygame.draw.rect(screen, DARK_BLUE, panel_rect)
        pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50), 2)

        # Жетоны
        screen.blit(self.token_icon, (10, 9))
        token_text = self.font.render(f"{self.player.total_tokens}", True, WHITE)
        screen.blit(token_text, (50, 15))

        # Энергия
        screen.blit(self.energy_icon, (200, 9))
        energy_text = self.font.render(f"{int(self.player.energy)}/{MAX_ENERGY}", True, WHITE)
        screen.blit(energy_text, (240, 15))

        # Курс и k
        course_text = self.small_font.render(f"Курс: {self.player.course}  k={self.player.k}", True, WHITE)
        screen.blit(course_text, (SCREEN_WIDTH - 200, 15))