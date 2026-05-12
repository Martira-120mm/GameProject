def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def format_number(num):
    """Форматирование числа с разделителями разрядов."""
    return f"{num:,}".replace(",", " ")