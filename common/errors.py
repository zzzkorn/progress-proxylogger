"""Ошибки"""


class ConfigError(Exception):
    """Исключение - ошибка при обработке конфигурации"""

    def __init__(self, attribute, error):
        self.attribute = attribute
        self.error = error

    def __str__(self):
        return f"{self.attribute} {self.error}"
