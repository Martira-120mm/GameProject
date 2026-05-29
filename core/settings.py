import os

MIN_WINDOW_WIDTH = 240
MIN_WINDOW_HEIGHT = 240
VIRTUAL_WIDTH = 1080    
VIRTUAL_HEIGHT = 720

SCREEN_WIDTH = VIRTUAL_WIDTH
SCREEN_HEIGHT = VIRTUAL_HEIGHT

FPS = 60

# Игровые константы
MAX_ENERGY = 100
ENERGY_REGEN_RATE = 1          # единиц в секунду
BASE_CLICKS_PER_TOKEN = 20
COURSE_THRESHOLDS = [800, 1200, 2000]
COURSE_N_VALUES = [0, 10, 20, 0]
UPGRADE_COST_MULTIPLIER = 100

# Автосохранение
AUTOSAVE_CLICKS_INTERVAL = 20

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
EXIT_BUTTON_COLOR = (180, 0, 0)

# Пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAVE_FILE_PATH = os.path.join(DATA_DIR, "save.json")
DIALOGS_FILE_PATH = os.path.join(DATA_DIR, "dialogs.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")






class DebugConfig:
    show_click_areas = False