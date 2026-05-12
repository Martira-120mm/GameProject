# core/game_state.py — единственный источник правды о состоянии игры

from settings import COURSE_N, BASE_CLICKS_REQUIRED, UPGRADE_PRICE_MULT


class GameState:
    """
    Хранит всё игровое состояние.
    Передаётся по ссылке во все сцены — они читают и изменяют его.
    """

    def __init__(self):
        self.tokens  = 0      # накопленные жетоны
        self.course  = 1      # текущий курс (1–4)
        self.k       = 1      # множитель жетонов за серию кликов
        self.clicks  = 0      # кол-во кликов в текущей серии

        # Флаг: только что получена награда — для анимации/вспышки в сцене
        self.reward_received = False

    # ------------------------------------------------------------------
    # Порог кликов для текущего курса
    # ------------------------------------------------------------------
    @property
    def clicks_required(self) -> int:
        """Сколько кликов нужно сделать, чтобы получить жетоны."""
        n = COURSE_N.get(self.course, 0)
        return BASE_CLICKS_REQUIRED + n

    # ------------------------------------------------------------------
    # Основная игровая механика
    # ------------------------------------------------------------------
    def add_click(self):
        """
        Засчитывает один клик.
        Если достигнут порог — начисляет жетоны и сбрасывает счётчик.
        """
        self.reward_received = False
        self.clicks += 1

        if self.clicks >= self.clicks_required:
            self.tokens += self.k
            self.clicks  = 0
            self.reward_received = True  # сцена узнает об этом в update()

    # ------------------------------------------------------------------
    # Апгрейд
    # ------------------------------------------------------------------
    @property
    def upgrade_price(self) -> int:
        """Цена следующего улучшения k."""
        return self.k * UPGRADE_PRICE_MULT

    def buy_upgrade(self) -> bool:
        """
        Пробует купить улучшение.
        Возвращает True при успехе, False — если не хватает жетонов.
        """
        price = self.upgrade_price
        if self.tokens >= price:
            self.tokens -= price
            self.k      += 1
            return True
        return False

    def can_upgrade(self) -> bool:
        """Проверяет, хватает ли жетонов на апгрейд."""
        return self.tokens >= self.upgrade_price

    # ------------------------------------------------------------------
    # Смена курса
    # ------------------------------------------------------------------
    def set_course(self, course: int):
        """Меняет курс (1–4) и сбрасывает счётчик кликов."""
        if course in COURSE_N:
            self.course = course
            self.clicks = 0

    # ------------------------------------------------------------------
    # Прогресс серии (0.0 … 1.0) — для прогресс-бара
    # ------------------------------------------------------------------
    @property
    def click_progress(self) -> float:
        return self.clicks / self.clicks_required if self.clicks_required > 0 else 0.0
