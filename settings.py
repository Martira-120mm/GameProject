# settings.py — все константы игры в одном месте

# --- Окно ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Дипломный клик"

# --- Цвета (R, G, B) ---
# Основные
COLOR_BG_OFFICE      = (30,  45,  60)   # тёмно-синий  — кабинет
COLOR_BG_CORRIDOR    = (45,  35,  55)   # тёмно-фиол.  — коридор
COLOR_BG_TUTOR       = (35,  55,  45)   # тёмно-зелён. — тьюторская

# UI-элементы
COLOR_PANEL          = (20,  20,  30)   # подложка панели
COLOR_PANEL_BORDER   = (80,  80, 120)   # рамка панели

# Кнопки
COLOR_BTN_NORMAL     = (60,  90, 150)   # обычная кнопка
COLOR_BTN_HOVER      = (80, 120, 200)   # наведение
COLOR_BTN_DISABLED   = (60,  60,  70)   # недоступна

COLOR_BTN_GREEN      = (50, 140,  80)   # кнопка "купить"
COLOR_BTN_GREEN_HVR  = (70, 180, 100)

COLOR_BTN_CLICK      = (180,  80,  60)  # главная кнопка клика
COLOR_BTN_CLICK_HVR  = (220, 110,  80)

# Текст
COLOR_TEXT_MAIN      = (220, 220, 230)  # основной текст
COLOR_TEXT_DIM       = (130, 130, 160)  # второстепенный текст
COLOR_TEXT_GOLD      = (240, 200,  60)  # жетоны
COLOR_TEXT_RED       = (230,  90,  90)  # предупреждения

# Прогресс-бар
COLOR_BAR_BG         = (40,  40,  55)
COLOR_BAR_FILL       = (70, 160, 230)

# --- Параметры игровой механики ---
# n добавки к порогу кликов в зависимости от курса
COURSE_N = {
    1: 0,
    2: 10,
    3: 20,
    4: 0,
}

BASE_CLICKS_REQUIRED = 20   # базовое кол-во кликов для получения жетонов
UPGRADE_PRICE_MULT   = 10   # цена апгрейда = k * UPGRADE_PRICE_MULT
