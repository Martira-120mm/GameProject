import pygame
import sys
import os

from core.settings import *
from core.game_state import StateManager
from core.resources import ResourceManager
from core.save_load import load_game, save_game
from entities.player import Player
from states.cabinet_state import CabinetState
from states.corridor_state import CorridorState
from states.tutor_state import TutorState
from states.ending_state import EndingState


def resource_path(relative_path):
    try:
        # Когда приложение запущено как EXE-файл, временная папка называется "_MEIPASS"
        base_path = sys._MEIPASS
    except Exception:
        # Когда приложение запущено как обычный скрипт (.py)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_scale_and_offset(real_size, virtual_size):
    """Возвращает масштаб и смещение, чтобы преобразовывать координаты."""
    real_w, real_h = real_size
    virt_w, virt_h = virtual_size
    scale = min(real_w / virt_w, real_h / virt_h)
    new_w = virt_w * scale
    new_h = virt_h * scale
    offset_x = (real_w - new_w) // 2
    offset_y = (real_h - new_h) // 2
    return scale, offset_x, offset_y


def virtualize_event(event, scale, offset_x, offset_y):
    """
    Создаёт новое событие мыши с координатами, пересчитанными в виртуальное пространство.
    Если событие не мышиное, возвращает оригинал.
    """
    if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        real_pos = event.pos
        virtual_x = (real_pos[0] - offset_x) / scale
        virtual_y = (real_pos[1] - offset_y) / scale
        # Округляем до целых, чтобы совпадало с целыми координатами rect'ов
        virtual_pos = (int(virtual_x), int(virtual_y))
        # Создаём новое событие, подменяя pos
        new_event = pygame.event.Event(event.type, **{k: v for k, v in event.dict.items() if k != 'pos'})
        new_event.pos = virtual_pos
        return new_event
    return event


def aspect_scale(virtual_surf, target_size):
    """Вписывает virtual_surf в target_size с сохранением пропорций."""
    virt_w, virt_h = virtual_surf.get_size()
    target_w, target_h = target_size
    scale = min(target_w / virt_w, target_h / virt_h)
    new_w = int(virt_w * scale)
    new_h = int(virt_h * scale)
    scaled = pygame.transform.scale(virtual_surf, (new_w, new_h))
    result = pygame.Surface(target_size)
    result.fill(BLACK)
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    result.blit(scaled, (x, y))
    return result


def initialize_game():
    """Инициализация Pygame, создание окна."""
    pygame.init()
    pygame.mixer.init()

    real_screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Дипломный клик")

    virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
    clock = pygame.time.Clock()

    ResourceManager.load_all()
    save_data = load_game(SAVE_FILE_PATH)
    player = Player(save_data)

    state_manager = StateManager()
    state_manager.add_state("cabinet", CabinetState(player, state_manager))
    state_manager.add_state("corridor", CorridorState(player, state_manager))
    state_manager.add_state("tutor", TutorState(player, state_manager))
    state_manager.add_state("ending", EndingState(player, state_manager))
    state_manager.change_state("tutor")

    return real_screen, virtual_screen, clock, state_manager, player


def main():
    real_screen, virtual_screen, clock, state_manager, player = initialize_game()
    running = True
    fullscreen = False
    window_size = [VIRTUAL_WIDTH, VIRTUAL_HEIGHT]

    while running:
        dt = clock.tick(FPS) / 1000.0

        # Получаем реальный размер окна
        real_size = real_screen.get_size()
        # Вычисляем параметры преобразования
        scale, off_x, off_y = get_scale_and_offset(real_size, (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

        # Обработка событий с пересчётом мышиных координат
        events = pygame.event.get()
        virtual_events = []
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        real_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        real_screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                elif event.key == pygame.K_F3:
                    from core.settings import DebugConfig
                    DebugConfig.show_click_areas = not DebugConfig.show_click_areas
                    print(f"[DEBUG] show_click_areas = {DebugConfig.show_click_areas}")
            elif event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    w, h = event.size
                    if w < MIN_WINDOW_WIDTH or h < MIN_WINDOW_HEIGHT:
                        w = max(w, MIN_WINDOW_WIDTH)
                        h = max(h, MIN_WINDOW_HEIGHT)
                        real_screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                    else:
                        real_screen = pygame.display.get_surface()
                    window_size = [w, h]
            else:
                # Преобразуем событие в виртуальные координаты
                virtual_event = virtualize_event(event, scale, off_x, off_y)
                virtual_events.append(virtual_event)

        # Передаём преобразованные события в состояния
        state_manager.handle_events(virtual_events)

        # Обновление логики
        state_manager.update(dt)

        # Отрисовка на виртуальный экран
        virtual_screen.fill(BLACK)
        state_manager.draw(virtual_screen)

        # Масштабирование и отображение
        final_screen = aspect_scale(virtual_screen, real_size)
        real_screen.blit(final_screen, (0, 0))
        pygame.display.flip()

    if not player.is_game_finished():
        save_game(player.to_dict(), SAVE_FILE_PATH)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()