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
from core.settings import DebugConfig 
import sys

class CabinetState(State):
    def __init__(self, player, state_manager):

        super().__init__()
        self.player = player
        self.state_manager = state_manager

        # Ресурсы
        self.bg = ResourceManager.get_image("cabinet_bg")
        #self.notebook_img = ResourceManager.get_image("notebook")
        self.token_icon = ResourceManager.get_image("token_icon")
        self.energy_icon = ResourceManager.get_image("energy_icon")
        self.font = ResourceManager.get_font("default")
        self.small_font = ResourceManager.get_font("small")

        # Область клика

        self.click_area = pygame.Rect(SCREEN_WIDTH/7.714 , SCREEN_HEIGHT/1.565, SCREEN_WIDTH/1.35, SCREEN_HEIGHT/2.88)

#      self.teacher_rect = pygame.Rect(50, SCREEN_HEIGHT - 350, 120, 200)
        self.teacher_img = ResourceManager.get_image("teacher")
        self.teacher_click_rect = pygame.Rect(SCREEN_WIDTH/6, SCREEN_HEIGHT/9, SCREEN_WIDTH/9, SCREEN_HEIGHT/3.27)
        self.teacher_hovered = False

        # Прогресс-бар
        bar_rect = pygame.Rect(SCREEN_WIDTH/2.918, SCREEN_HEIGHT/1.8, SCREEN_WIDTH/3.6, SCREEN_HEIGHT/36)
        self.progress_bar = ProgressBar(bar_rect, 1)

        # Кнопка коридор
        btn_rect = pygame.Rect(
            SCREEN_WIDTH / 1.227,
            SCREEN_HEIGHT / 7.2,
            SCREEN_WIDTH / 9,
            SCREEN_HEIGHT / 3.2
        )
        self.button_corridor = Button(
            btn_rect, "Коридор", self.go_to_corridor,
            alpha=51,
            normal_color=GRAY, hover_color=LIGHT_GRAY, pressed_color=BLUE,
            text_color=BLACK
        )

        self.quit_button = Button(
            pygame.Rect(SCREEN_WIDTH - 70, 10, 60, 30),
            "Выход", self.quit_game,
            font=self.small_font,
            normal_color=RED, hover_color=(255, 80, 80), pressed_color=(150, 0, 0),
            text_color=WHITE
        )

        # Звуки
        self.click_sound = ResourceManager.get_sound("click")
        self.token_sound = ResourceManager.get_sound("token")
        self.fanfare_sound = ResourceManager.get_sound("fanfare")

        # Автосохранение
        self.clicks_since_autosave = 0

        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dialog_box = DialogBox(screen_rect)

    def quit_game(self):
        save_game(self.player.to_dict(), SAVE_FILE_PATH)
        pygame.quit()
        sys.exit()

    def go_to_corridor(self):
        self.state_manager.change_state("corridor")

    def _show_teacher_dialog(self):
        phrases = ResourceManager.get_dialog("teacher", "idle")
        if phrases:
            text = random.choice(phrases)
        else:
            text = "Пишите, студент! Каждый клик приближает вас к диплому."

        # Размеры и позиция
        teacher_width = 200
        teacher_height = 300

        # Вычисляем доступное место
        max_dialog_width = SCREEN_WIDTH - teacher_width - 80   # 80 = отступы слева и между
        dialog_width = min(500, max_dialog_width)               # ограничиваем ширину
        dialog_height = 180

        # Учитель слева по центру
        teacher_x = 30
        teacher_y = SCREEN_HEIGHT // 2 - teacher_height // 2

        # Диалог справа от учителя
        dialog_x = teacher_x + teacher_width + 90
        dialog_y = SCREEN_HEIGHT // 2 - dialog_height // 2

        # Корректируем диалог, чтобы не вылезал за правый край
        if dialog_x + dialog_width > SCREEN_WIDTH:
            dialog_x = SCREEN_WIDTH - dialog_width - 10
            # Учителя сдвигаем левее, если диалог упирается в край
            teacher_x = dialog_x - teacher_width - 20
            if teacher_x < 10:
                teacher_x = 10

        # Не даём диалогу вылезти за верхнюю/нижнюю границу
        dialog_y = max(10, dialog_y)
        if dialog_y + dialog_height > SCREEN_HEIGHT - 10:
            dialog_y = SCREEN_HEIGHT - dialog_height - 10

        # Сохраняем исходный rect диалога (если ещё не сохранён)
        if not hasattr(self, 'dialog_original_rect'):
            self.dialog_original_rect = self.dialog_box.rect.copy()

        # Перемещаем и показываем диалог
        self.dialog_box.rect.topleft = (dialog_x, dialog_y)
        self.dialog_box.show_text(text, speaker="Преподаватель")

        # Запоминаем rect для отрисовки преподавателя
        self.dialog_teacher_rect = pygame.Rect(teacher_x, teacher_y, teacher_width, teacher_height)

    def handle_events(self, events):
        for event in events:
            if self.dialog_box.active:
                self.dialog_box.handle_event(event)
                continue
            self.quit_button.handle_event(event)
            self.button_corridor.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.teacher_click_rect.collidepoint(event.pos):
                    self._show_teacher_dialog()
                elif self.click_area.collidepoint(event.pos):
                    self._handle_click()
            elif event.type == pygame.MOUSEMOTION:
                # Проверяем наведение на учителя и тетрадь
                self.teacher_hovered = self.teacher_click_rect.collidepoint(event.pos)
                if self.teacher_hovered or self.click_area.collidepoint(event.pos):
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
        if self.click_sound:
            self.click_sound.play()

        if token_earned:
            if self.token_sound:
                self.token_sound.play()
            if self.player.is_game_finished():
                if self.fanfare_sound:
                    self.fanfare_sound.play()
                self.state_manager.change_state("ending")
                return

        # Обновляем прогресс-бар после клика
        self._update_progress_bar()

        # Автосохранение
        self.clicks_since_autosave += 1
        if self.clicks_since_autosave >= AUTOSAVE_CLICKS_INTERVAL:
            save_game(self.player.to_dict(), SAVE_FILE_PATH)
            self.clicks_since_autosave = 0

    def _draw_click_area(self, screen):
        """Отрисовывает зону клика с цветными уголками."""
        rect = self.click_area
        # Полупрозрачный фон (едва заметный)
        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 50))  # серый с прозрачностью
        screen.blit(overlay, rect.topleft)

        # Цветные уголки
        corner_color = RED
        corner_length = 20
        thickness = 4

        # Верхний левый угол
        pygame.draw.line(screen, corner_color, rect.topleft, (rect.left + corner_length, rect.top), thickness)
        pygame.draw.line(screen, corner_color, rect.topleft, (rect.left, rect.top + corner_length), thickness)

        # Верхний правый угол
        pygame.draw.line(screen, corner_color, rect.topright, (rect.right - corner_length, rect.top), thickness)
        pygame.draw.line(screen, corner_color, rect.topright, (rect.right, rect.top + corner_length), thickness)

        # Нижний левый угол
        pygame.draw.line(screen, corner_color, rect.bottomleft, (rect.left + corner_length, rect.bottom), thickness)
        pygame.draw.line(screen, corner_color, rect.bottomleft, (rect.left, rect.bottom - corner_length), thickness)

        # Нижний правый угол
        pygame.draw.line(screen, corner_color, rect.bottomright, (rect.right - corner_length, rect.bottom), thickness)
        pygame.draw.line(screen, corner_color, rect.bottomright, (rect.right, rect.bottom - corner_length), thickness)


        # Автосохранение
        self.clicks_since_autosave += 1
        if self.clicks_since_autosave >= AUTOSAVE_CLICKS_INTERVAL:
            save_game(self.player.to_dict(), SAVE_FILE_PATH)
            self.clicks_since_autosave = 0

    def _draw_teacher_area(self, screen):
        rect = self.teacher_click_rect
        # Фон с подсветкой
        if self.teacher_hovered:
            fill_color = (80, 80, 80, 100)  # светлее
        else:
            fill_color = (30, 30, 30, 100)  # темнее
        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        overlay.fill(fill_color)
        screen.blit(overlay, rect.topleft)

        # Зелёные уголки
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

    def _update_progress_bar(self):
        total_needed = Progression.calc_clicks_for_token(self.player.k, self.player.n)
        done = total_needed - self.player.clicks_until_token
        self.progress_bar.set_values(done, total_needed)

    def update(self, dt):
        if self.dialog_box.active:
            self.dialog_box.update(dt)
        else:
            # Возвращаем исходную позицию и размеры диалога
            if hasattr(self, 'dialog_original_rect'):
                self.dialog_box.rect = self.dialog_original_rect.copy()
                if hasattr(self, 'dialog_original_width'):
                    self.dialog_box.width = self.dialog_original_width
                    self.dialog_box.rect.width = self.dialog_original_width
                    del self.dialog_original_width
                del self.dialog_original_rect

            self.quit_button.update(dt)
            self.player.update_energy(dt)
            self.button_corridor.update(dt)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        if not self.dialog_box.active:
            self.button_corridor.draw(screen)

        if not self.dialog_box.active:
            if DebugConfig.show_click_areas:
                self._draw_click_area(screen)
                self._draw_teacher_area(screen)
        
        self._draw_resource_panel(screen)
        self.progress_bar.draw(screen)

        # Затемнение и диалоговое окно
        self.dialog_box.draw(screen)

        # Большой преподаватель строго поверх затемнения (только при активном диалоге)
        if self.dialog_box.active and hasattr(self, 'dialog_teacher_rect') and self.teacher_img is not None:
            scaled_teacher = pygame.transform.scale(self.teacher_img, self.dialog_teacher_rect.size)
            screen.blit(scaled_teacher, self.dialog_teacher_rect.topleft)
        self.quit_button.draw(screen)

    def _get_battery_image(self):
        percent = self.player.energy / MAX_ENERGY
        images = ResourceManager.get_image("battery")
        if not images:
            return self.energy_icon   # запасная иконка
        if percent <= 0.33:
            return images[0]
        elif percent <= 0.66:
            return images[1]
        else:
            return images[2]

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
        battery_img = self._get_battery_image()
        screen.blit(battery_img, (200, 9))
        energy_text = self.font.render(f"{int(self.player.energy)}/{MAX_ENERGY}", True, WHITE)
        screen.blit(energy_text, (240, 15))

        item_text = self.font.render(f"Математика", True, WHITE)
        screen.blit(item_text, (400, 15))
        
        # Курс и k
        course_text = self.small_font.render(f"Курс: {self.player.course}  k={self.player.k}", True, WHITE)
        screen.blit(course_text, (SCREEN_WIDTH - 200, 15))

