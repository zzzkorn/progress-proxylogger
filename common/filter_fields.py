from common.comparators import is_mapped


def serialize(filter, value):
    if is_mapped(value):
        return {"id": value.id}
    return value


class Field:
    """Поле для фильтрации оп значению поля таблицы

    Parameters
    ----------
    field : inst of :class:`sqlalchemy.schema.Column`
        Поле по которому будет происходить фильтрация
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, query, value):
        """Метод добавляет в query фильтр

        Parameters
        ----------
        query : inst of :class:`sqlalchemy.orm.query.Query`
            Исходный query
        value : any
            Значение фильтра

        Returns
        -------
        query : inst of :class:`sqlalchemy.orm.query.Query`
            Query с добавленой сортировкой
        """
        if value is None:
            return query
        return query.filter(self.field == value)


class BooleanSelect(Field):
    """Поля для поиска по булевому значению

    Parameters
    ----------
    field : list of inst of :class:`sqlalchemy.schema.Column`
        Поле по которому будет происходить фильтрация
    """

    def __call__(self, query, value):
        if value is None:
            return query
        try:
            value = bool(int(value))
        except ValueError:
            return query
        return query.filter(self.field == value)
