from core.settings import BASE_CLICKS_PER_TOKEN

class Progression:
    @staticmethod
    def calc_clicks_for_token(k, n):
        return BASE_CLICKS_PER_TOKEN + n + k

    @staticmethod
    def get_course_threshold(course):
        from core.settings import COURSE_THRESHOLDS
        if 1 <= course < 4:
            return COURSE_THRESHOLDS[course - 1]
        return None

    @staticmethod
    def get_n_for_course(course):
        from core.settings import COURSE_N_VALUES
        if 1 <= course <= 4:
            return COURSE_N_VALUES[course - 1]
        return 0