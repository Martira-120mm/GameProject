class State:
    """Базовый класс для всех игровых состояний."""
    def __init__(self):
        self.state_manager = None

    def on_enter(self, **kwargs):
        """Вызывается при входе в состояние."""
        pass

    def on_exit(self):
        """Вызывается при выходе из состояния."""
        pass

    def handle_events(self, events):
        """Обработка событий Pygame."""
        pass

    def update(self, dt):
        """Обновление логики, dt - время с прошлого кадра в секундах."""
        pass

    def draw(self, screen):
        """Отрисовка состояния."""
        pass


class StateManager:
    """Управляет состояниями игры."""
    def __init__(self):
        self.states = {}
        self.active_state = None

    def add_state(self, name, state):
        self.states[name] = state
        state.state_manager = self

    def change_state(self, name, **kwargs):
        if self.active_state:
            self.active_state.on_exit()
        self.active_state = self.states[name]
        self.active_state.on_enter(**kwargs)

    def handle_events(self, events):
        if self.active_state:
            self.active_state.handle_events(events)

    def update(self, dt):
        if self.active_state:
            self.active_state.update(dt)

    def draw(self, screen):
        if self.active_state:
            self.active_state.draw(screen)