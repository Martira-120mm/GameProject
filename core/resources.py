import pygame
import json
import os
from core.settings import *

class ResourceManager:
    images = {}
    sounds = {}
    fonts = {}
    dialogs = {}

    @classmethod
    def load_all(cls):
        cls._load_dialogs()
        cls._load_fonts()
        cls._load_images()
        cls._load_sounds()  # теперь метод существует

    @classmethod
    def _get_assets_path(cls, subfolder=""):
        return os.path.join(BASE_DIR, "assets", subfolder)

    @classmethod
    def _load_image(cls, filename, target_size=None, fallback_color=None, fit_mode="stretch"):
        """Загружает изображение с автоматическим масштабированием."""
        path = os.path.join(cls._get_assets_path("images"), filename)
        try:
            img = pygame.image.load(path).convert_alpha()
            original_size = img.get_size()
            if target_size and original_size != target_size:
                if fit_mode == "stretch":
                    img = pygame.transform.scale(img, target_size)
                elif fit_mode == "contain":
                    img = cls._fit_contain(img, target_size)
                elif fit_mode == "cover":
                    img = cls._fit_cover(img, target_size)
                else:
                    img = pygame.transform.scale(img, target_size)
            return img
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️ Не удалось загрузить '{filename}': {e}")
            if fallback_color and target_size:
                surf = pygame.Surface(target_size, pygame.SRCALPHA)
                surf.fill(fallback_color)
                return surf
            return None

    @staticmethod
    def _fit_contain(surface, target_size):
        surf_rect = surface.get_rect()
        target_rect = pygame.Rect(0, 0, *target_size)
        scale = min(target_rect.width / surf_rect.width, target_rect.height / surf_rect.height)
        new_size = (int(surf_rect.width * scale), int(surf_rect.height * scale))
        scaled = pygame.transform.scale(surface, new_size)
        result = pygame.Surface(target_size, pygame.SRCALPHA)
        result.fill((0, 0, 0, 0))
        pos = ((target_size[0] - new_size[0]) // 2, (target_size[1] - new_size[1]) // 2)
        result.blit(scaled, pos)
        return result

    @staticmethod
    def _fit_cover(surface, target_size):
        surf_rect = surface.get_rect()
        target_rect = pygame.Rect(0, 0, *target_size)
        scale = max(target_rect.width / surf_rect.width, target_rect.height / surf_rect.height)
        new_size = (int(surf_rect.width * scale), int(surf_rect.height * scale))
        scaled = pygame.transform.scale(surface, new_size)
        result = pygame.Surface(target_size, pygame.SRCALPHA)
        result.fill((0, 0, 0, 0))
        pos = ((target_size[0] - new_size[0]) // 2, (target_size[1] - new_size[1]) // 2)
        result.blit(scaled, pos)
        return result

    @classmethod
    def _load_images(cls):
        # Фоны
        cls.images["cabinet_bg"] = cls._load_image(
            "cabinet_bg.png", (SCREEN_WIDTH, SCREEN_HEIGHT), (100, 100, 150), fit_mode="cover"
        )
        cls.images["corridor_bg"] = cls._load_image(
            "corridor_bg.png", (SCREEN_WIDTH, SCREEN_HEIGHT), (150, 100, 100), fit_mode="cover"
        )
        cls.images["tutor_bg"] = cls._load_image(
            "tutor_bg.png", (SCREEN_WIDTH, SCREEN_HEIGHT), (100, 150, 100), fit_mode="cover"
        )

        # Тетрадь
        cls.images["notebook"] = cls._load_image(
            "notebook.png", (200, 280), (200, 200, 255), fit_mode="stretch"
        )

        # Иконки
        cls.images["token_icon"] = cls._load_image(
            "token_icon.png", (32, 32), (255, 215, 0)
        )
        cls.images["energy_icon"] = cls._load_image(
            "energy_icon.png", (32, 32), (0, 255, 0)
        )

        # Батарейки
        battery_sizes = (32, 32)
        cls.images["battery"] = [
            cls._load_image("battery_0.png", battery_sizes, (255, 0, 0)),
            cls._load_image("battery_20.png", battery_sizes, (255, 165, 0)),
            cls._load_image("battery_40.png", battery_sizes, (255, 255, 0)),
            cls._load_image("battery_60.png", battery_sizes, (173, 255, 47)),
            cls._load_image("battery_80.png", battery_sizes, (0, 255, 0)),
        ]

        # Персонажи
        cls.images["teacher"] = cls._load_image(
            "teacher.png", (120, 200), (200, 150, 150), fit_mode="contain"
        )
        cls.images["tutor"] = cls._load_image(
            "tutor.png", (120, 200), (150, 200, 150), fit_mode="contain"
        )

        # Кнопки (если есть)
        cls.images["button_corridor"] = cls._load_image(
            "button_corridor.png", (150, 50), (180, 180, 180)
        )

    @classmethod
    def _load_sounds(cls):
        """Загрузка звуков (пока заглушки)."""
        # В реальном проекте здесь была бы загрузка .wav/.ogg
        cls.sounds["click"] = None
        cls.sounds["token"] = None
        cls.sounds["fanfare"] = None
        cls.sounds["ambient"] = None

    @classmethod
    def _load_dialogs(cls):
        try:
            with open(DIALOGS_FILE_PATH, 'r', encoding='utf-8') as f:
                cls.dialogs = json.load(f)
        except FileNotFoundError:
            cls.dialogs = {
                "teacher": {
                    "idle": ["Пишите, студент!", "Ещё немного..."],
                    "token_earned": ["Жетон получен!"]
                },
                "tutor": {
                    "greeting": ["Легкой учёбы!"]
                },
                "course_upgrade": {
                    "2": "Поздравляем с переходом на 2 курс!",
                    "3": "Вы на 3 курсе!",
                    "4": "Последний курс — финишная прямая!"
                },
                "ending": {
                    "title": "Защита диплома",
                    "congratulations": "Защита прошла успешно! Поздравляем с получением диплома.",
                    "credits": ["Разработчик: Команда DiplomaClick", "Художник: Аниме-стиль"]
                }
            }

    @classmethod
    def _load_fonts(cls):
        cls.fonts["default"] = pygame.font.Font(None, 32)
        cls.fonts["small"] = pygame.font.Font(None, 24)
        cls.fonts["large"] = pygame.font.Font(None, 48)

    @classmethod
    def get_image(cls, key):
        return cls.images.get(key)

    @classmethod
    def get_sound(cls, key):
        return cls.sounds.get(key)

    @classmethod
    def get_font(cls, key="default"):
        return cls.fonts.get(key, cls.fonts["default"])

    @classmethod
    def get_dialog(cls, *keys):
        data = cls.dialogs
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, "")
            else:
                return ""
        return data