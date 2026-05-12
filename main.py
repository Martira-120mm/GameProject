# main.py — точка входа в игру

import pygame
import sys

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from core.game_state   import GameState
from core.scene_manager import SceneManager
from scenes.office     import OfficeScene
from scenes.tutor_room import TutorRoomScene
from scenes.corridor   import CorridorScene


def main():
    # ------------------------------------------------------------------
    # 1. Инициализация pygame
    # ------------------------------------------------------------------
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # ------------------------------------------------------------------
    # 2. Создание общего состояния игры
    # ------------------------------------------------------------------
    game_state = GameState()

    # ------------------------------------------------------------------
    # 3. Создание SceneManager и регистрация всех сцен
    #    Каждая сцена получает ссылку на game_state
    # ------------------------------------------------------------------
    manager = SceneManager()
    manager.register("office",    OfficeScene(game_state))
    manager.register("tutor_room", TutorRoomScene(game_state))
    manager.register("corridor",  CorridorScene(game_state))

    # Стартовая сцена — кабинет
    manager.set_start("office")

    # ------------------------------------------------------------------
    # 4. Главный игровой цикл
    # ------------------------------------------------------------------
    running = True
    while running:
        # --- Сбор событий ---
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # Выход по Escape
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- Передаём события в активную сцену ---
        manager.handle_events(events)

        # --- Обновляем логику активной сцены ---
        manager.update()

        # --- Рисуем активную сцену ---
        manager.draw(screen)

        # --- Показываем кадр на экране ---
        pygame.display.flip()

        # --- Ограничиваем FPS ---
        clock.tick(FPS)

    # ------------------------------------------------------------------
    # 5. Завершение
    # ------------------------------------------------------------------
    pygame.quit()
    sys.exit()


# Запуск только если файл запущен напрямую (не импортирован)
if __name__ == "__main__":
    main()
