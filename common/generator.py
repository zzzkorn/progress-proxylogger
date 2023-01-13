import logging
import random
from functools import wraps


def func_has_arg(function, arg_name):
    code = function.__code__
    var_names = code.co_varnames
    arg_count = code.co_argcount + code.co_kwonlyargcount
    args = var_names[:arg_count]

    return arg_name in args


def optional_args(f, *optional_arg_list):
    def deco(foo):
        def wrapper(*args, **kwargs):
            optional = dict()
            for optional_arg in optional_arg_list:
                value = kwargs.pop(optional_arg, None)
                if func_has_arg(f, optional_arg):
                    optional[optional_arg] = value

            return foo(*args, **optional, **kwargs)

        return wrapper

    return deco


class Custom(object):
    """
    Генератор, который запускает кастомные функции.
    Использование:

    >>> generator: Generator
    >>> @generator.custom()
    >>> def foo(session):
    >>>     pass
    >>>

    у custom опциональные параметры:
        - count - количество запусков функции
        - variants - список словарей - варианты запуска функции

    >>> @generator.custom(
    >>>     count=2,
    >>>     variants=[{'bar': 1}, {'bar': 2}],
    >>> )
    >>> def foo(session, variant):
    >>>     # variant - необязательный параметр
    >>>     bar = variant['bar']
    >>>     print(f'generate some with {bar}!')
    >>>     return bar
    >>>

    У функции, декорированной @generator.custom(), есть атрибут generated.

    В случае, если variants не использованы, содержит список возвращенных
    при запуске функции значений
    (сколько count, столько и элементов в generated)

    В случае, если использованы variants, то в generated будет лежать список
    variants, для каждого элемента будут добавлены ключи
       - count: количество запусков
       - returned: возвращенные значения для данного варианта
    """

    registered = []
    optional_args = ["variant"]

    @classmethod
    def run(cls, session):

        for f in cls.registered:
            msg = f.__doc__ or f"Run custom generator function: {f.__name__}"
            counts = f"x{f.count} times"
            if f.variants:
                counts = f"{counts} x{len(f.variants)} variants"
            logging.info(f"{msg} ({counts})")

            if f.variants:
                result = []
                for variant in f.variants:
                    variant["count"] = f.count
                    variant["returned"] = []
                    for _ in range(f.count):
                        returned = f(session=session, variant=variant)
                        cls.add_results(returned, variant["returned"])
                    session.commit()
                    result.append(variant)
                f.generated = result
            else:
                for _ in range(f.count):
                    result = f(session=session)
                    cls.add_results(result, f.generated)
                session.commit()

    @staticmethod
    def add_results(result, store):

        if isinstance(result, list):
            store.extend(result)
        else:
            store.append(result)

    def __init__(self, count=1, variants=False):
        self.count = count
        self.variants = variants

    def __call__(self, f):
        @wraps(f)
        @optional_args(f, *self.optional_args)
        def wrapper(session, **kwargs):
            return f(session, **kwargs)

        wrapper.count = self.count
        wrapper.variants = self.variants
        wrapper.generated = []
        self.registered.append(wrapper)
        return wrapper


class Generator(object):
    def __init__(self):
        self.custom = type("Custom", (Custom,), dict())

    def __call__(self, session):
        self.custom.run(session)


class RelationFK:
    def __call__(self, session, model):
        items = session.query(model).all()
        if not items:
            return None
        chosen = random.choice(items)
        return chosen
