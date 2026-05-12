import pygame
import sys

from core.settings import *
from core.game_state import StateManager
from core.resources import ResourceManager
from core.save_load import load_game, save_game
from entities.player import Player
from states.cabinet_state import CabinetState
from states.corridor_state import CorridorState
from states.tutor_state import TutorState
from states.ending_state import EndingState


def initialize_game():
    """Инициализация Pygame, создание окна, загрузка ресурсов и состояний."""
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Дипломный клик")
    clock = pygame.time.Clock()

    # Загрузка ресурсов (в текущей версии заглушки)
    ResourceManager.load_all()

    # Попытка загрузить сохранение
    save_data = load_game(SAVE_FILE_PATH)
    player = Player(save_data)

    # Создание менеджера состояний
    state_manager = StateManager()

    # Регистрация состояний
    state_manager.add_state("cabinet", CabinetState(player, state_manager))
    state_manager.add_state("corridor", CorridorState(player, state_manager))
    state_manager.add_state("tutor", TutorState(player, state_manager))
    state_manager.add_state("ending", EndingState(player, state_manager))

    # Начальное состояние - кабинет
    state_manager.change_state("cabinet")

    return screen, clock, state_manager, player


def main():
    screen, clock, state_manager, player = initialize_game()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0  # время в секундах с прошлого кадра

        # Обработка событий
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            else:
                state_manager.handle_events([event])

        # Обновление
        state_manager.update(dt)

        # Отрисовка
        screen.fill(BLACK)
        state_manager.draw(screen)
        pygame.display.flip()

    # Автосохранение при выходе
    if not player.is_game_finished():
        save_game(player.to_dict(), SAVE_FILE_PATH)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()