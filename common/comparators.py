from datetime import date
from datetime import datetime

from sqlalchemy.orm import object_mapper
from sqlalchemy.orm.exc import UnmappedInstanceError

date_format = "%Y-%m-%d"


def is_mapped(obj):
    try:
        object_mapper(obj)
    except UnmappedInstanceError:
        return False
    return True


def normalize_value(value):
    if isinstance(value, datetime) or isinstance(value, date):
        value = value.strftime(date_format)
    if is_mapped(value):
        value = dict(id=value.id)
    if isinstance(value, dict) and "id" in value:
        value = dict(id=value.get("id"))
    if isinstance(value, list):
        value = [normalize_value(e) for e in value]
    return value


def check_values(value_1, value_2):
    value_1 = normalize_value(value_1)
    value_2 = normalize_value(value_2)
    assert value_1 == value_2


def compare_fields(body, response, exclude_fields=()):
    for key, value in body.items():
        if key not in exclude_fields:
            value_in_db = (
                response.get(key)
                if isinstance(response, dict)
                else getattr(response, key)
            )
            check_values(value_in_db, value)
