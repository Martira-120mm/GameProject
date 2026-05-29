from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT 
def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def format_number(num):
    """Форматирование числа с разделителями разрядов."""
    return f"{num:,}".replace(",", " ")

def rel_x(x_base, base_w=SCREEN_WIDTH):
    return int(SCREEN_WIDTH * x_base / base_w)

def rel_y(y_base, base_h=SCREEN_HEIGHT):
    return int(SCREEN_HEIGHT * y_base / base_h)