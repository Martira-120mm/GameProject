from core.settings import *
from entities.progression import Progression

class Player:
    def __init__(self, data=None):
        if data:
            self.total_tokens = data.get("total_tokens", 0)
            self.k = data.get("k", 1)
            self.course = data.get("course", 1)
            self.energy = data.get("energy", MAX_ENERGY)
            self.clicks_until_token = data.get("clicks_until_token", 0)
        else:
            self.total_tokens = 0
            self.k = 1
            self.course = 1
            self.energy = MAX_ENERGY
            self.clicks_until_token = Progression.calc_clicks_for_token(self.k, self._get_n())

        # Убедимся, что n соответствует курсу
        self._update_n()

    def _get_n(self):
        return COURSE_N_VALUES[self.course - 1]

    def _update_n(self):
        self.n = self._get_n()

    def to_dict(self):
        return {
            "total_tokens": self.total_tokens,
            "k": self.k,
            "course": self.course,
            "energy": self.energy,
            "clicks_until_token": self.clicks_until_token
        }

    def can_click(self):
        return self.energy >= 1.0

    def perform_click(self):
        """Обрабатывает один клик. Возвращает True, если был получен жетон."""
        if not self.can_click():
            return False

        self.energy = max(0.0, self.energy - 1.0)
        self.clicks_until_token -= 1

        token_earned = False
        if self.clicks_until_token <= 0:
            self._grant_token()
            token_earned = True

        return token_earned

    def _grant_token(self):
        self.total_tokens += 1
        self.clicks_until_token = Progression.calc_clicks_for_token(self.k, self.n)
        self._check_course_upgrade()

    def _check_course_upgrade(self):
        """Проверяет и выполняет переход на следующий курс, возвращает True, если переход был."""
        upgraded = False
        while self.course < 4 and self.total_tokens >= COURSE_THRESHOLDS[self.course - 1]:
            self.course += 1
            self._update_n()
            self.clicks_until_token = Progression.calc_clicks_for_token(self.k, self.n)
            upgraded = True
        return upgraded

    def update_energy(self, dt):
        self.energy = min(MAX_ENERGY, self.energy + ENERGY_REGEN_RATE * dt)

    def can_buy_upgrade(self):
        return self.total_tokens >= self.upgrade_cost()

    def upgrade_cost(self):
        return UPGRADE_COST_MULTIPLIER * (self.k ** 2)

    def buy_upgrade(self):
        if not self.can_buy_upgrade():
            return False
        self.total_tokens -= self.upgrade_cost()
        self.k += 1
        self.clicks_until_token = Progression.calc_clicks_for_token(self.k, self.n)
        return True

    def is_game_finished(self):
        return self.course == 4 and self.total_tokens >= COURSE_THRESHOLDS[2]