# scenes/base_scene.py — абстрактный базовый класс для всех сцен


class BaseScene:
    """
    Каждая сцена ОБЯЗАНА реализовать три метода:
        handle_events(events) → str | None
        update()              → str | None
        draw(screen)          → None

    Возвращение строки из handle_events или update — сигнал SceneManager'у
    переключиться на сцену с таким именем.
    """

    def __init__(self, game_state):
        self.state = game_state  # ссылка на общее состояние игры

    def handle_events(self, events):
        """Обрабатывает события pygame. Возвращает имя следующей сцены или None."""
        raise NotImplementedError

    def update(self):
        """Обновляет логику. Возвращает имя следующей сцены или None."""
        raise NotImplementedError

    def draw(self, screen):
        """Рисует всё на экране."""
        raise NotImplementedError
