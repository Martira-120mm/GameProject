# core/scene_manager.py — управляет переключением между сценами


class SceneManager:
    """
    Хранит словарь всех сцен и знает, какая сцена сейчас активна.

    Сцена сигнализирует о переходе, возвращая строку-имя из handle_events().
    SceneManager перехватывает это и делает нужную сцену текущей.
    """

    def __init__(self):
        self._scenes: dict  = {}   # {"office": OfficeScene, ...}
        self._current: str  = ""   # имя активной сцены

    # ------------------------------------------------------------------
    # Регистрация сцен
    # ------------------------------------------------------------------
    def register(self, name: str, scene):
        """Добавить сцену под именем name."""
        self._scenes[name] = scene

    def set_start(self, name: str):
        """Установить начальную сцену (вызывается один раз из main.py)."""
        self._current = name

    # ------------------------------------------------------------------
    # Игровой цикл — вызывается из main.py
    # ------------------------------------------------------------------
    def handle_events(self, events):
        scene = self._get_current()
        if scene is None:
            return

        next_scene = scene.handle_events(events)

        # Если сцена вернула строку — переключаемся
        if isinstance(next_scene, str) and next_scene in self._scenes:
            self._current = next_scene

    def update(self):
        scene = self._get_current()
        if scene:
            next_scene = scene.update()
            if isinstance(next_scene, str) and next_scene in self._scenes:
                self._current = next_scene

    def draw(self, screen):
        scene = self._get_current()
        if scene:
            scene.draw(screen)

    # ------------------------------------------------------------------
    # Вспомогательное
    # ------------------------------------------------------------------
    def _get_current(self):
        return self._scenes.get(self._current)
