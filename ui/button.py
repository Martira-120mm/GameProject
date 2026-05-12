# ui/button.py — переиспользуемый компонент кнопки

import pygame
from settings import COLOR_BTN_NORMAL, COLOR_BTN_HOVER, COLOR_BTN_DISABLED, COLOR_TEXT_MAIN


class Button:
    """
    Прямоугольная кнопка с текстом.

    Параметры:
        x, y        — позиция левого верхнего угла
        width, height
        text        — надпись на кнопке
        color       — обычный цвет фона
        hover_color — цвет при наведении мыши
        font        — pygame.font.Font (если None — создаётся дефолтный)
        enabled     — если False, кнопка серая и не реагирует на клики
    """

    def __init__(
        self,
        x: int, y: int,
        width: int, height: int,
        text: str,
        color=COLOR_BTN_NORMAL,
        hover_color=COLOR_BTN_HOVER,
        font: pygame.font.Font = None,
        enabled: bool = True,
    ):
        self.rect        = pygame.Rect(x, y, width, height)
        self.text        = text
        self.color       = color
        self.hover_color = hover_color
        self.enabled     = enabled

        # Если шрифт не передан — создаём системный
        self.font = font or pygame.font.SysFont("segoeui", 20)

    # ------------------------------------------------------------------
    # Проверка клика
    # ------------------------------------------------------------------
    def is_clicked(self, events) -> bool:
        """
        Возвращает True, если в списке событий есть клик мышью по кнопке.
        Принимает список pygame-событий из игрового цикла.
        """
        if not self.enabled:
            return False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False

    # ------------------------------------------------------------------
    # Отрисовка
    # ------------------------------------------------------------------
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Выбираем цвет
        if not self.enabled:
            bg_color = COLOR_BTN_DISABLED
        elif self.rect.collidepoint(mouse_pos):
            bg_color = self.hover_color
        else:
            bg_color = self.color

        # Фон кнопки
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)

        # Рамка
        border_color = (255, 255, 255, 60) if self.enabled else (80, 80, 80)
        pygame.draw.rect(screen, border_color, self.rect, width=1, border_radius=8)

        # Текст — центрируем
        text_surf = self.font.render(self.text, True, COLOR_TEXT_MAIN)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
