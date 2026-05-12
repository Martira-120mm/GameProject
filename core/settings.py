import os

# Окно
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 60

# Игровые константы
MAX_ENERGY = 100
ENERGY_REGEN_RATE = 10          # единиц в секунду
BASE_CLICKS_PER_TOKEN = 20
COURSE_THRESHOLDS = [800, 1200, 2000]   # пороги жетонов для перехода на 2,3,4 курсы
COURSE_N_VALUES = [0, 10, 20, 0]        # n для курсов 1..4 (индекс 0 = 1 курс)
UPGRADE_COST_MULTIPLIER = 100

# Автосохранение
AUTOSAVE_CLICKS_INTERVAL = 20     # каждые 20 кликов

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 128)

# Пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAVE_FILE_PATH = os.path.join(DATA_DIR, "save.json")
DIALOGS_FILE_PATH = os.path.join(DATA_DIR, "dialogs.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")