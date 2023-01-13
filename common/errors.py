"""Ошибки"""


class ConfigError(Exception):
    """Ошибка при обработке параметра конфигурации

    Parameters
    ----------
    attribute : str
       Атрибут
    message : str
       Текст ошибки
    """

    def __init__(self, attribute, message):
        self.attribute = attribute
        self.message = message

    def __str__(self):
        return (
            f"Ошибка при обработке параметра конфигурации "
            f"{self.attribute}: {self.message}"
        )


class ObjectNotFound(Exception):
    """Объект не найден

    Parameters
    ----------
    model : sqlalchemy model
       Класс модели
    obj_id : int
       Идентификатор объекта
    """

    def __init__(self, model, obj_id):
        self.model = model
        self.obj_id = obj_id

    def __str__(self):
        return f"Объект {self.model.__name__}(id={self.obj_id}) не найден"
