"""Кофнфигурация логера"""
import logging
import os
import sys
from logging import handlers

from common.variables import ENCODING
from common.variables import LOGGING_LEVEL

MAIN_FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(PATH, "logger.log")
ERR_PATH = os.path.join(PATH, "logger_err.log")

# создаём потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stdout)
STREAM_HANDLER.setFormatter(MAIN_FORMATTER)
STREAM_HANDLER.setLevel(LOGGING_LEVEL)

LOG_FILE = handlers.TimedRotatingFileHandler(
    LOG_PATH,
    encoding=ENCODING,
    interval=1,
    when="D",
)
LOG_FILE.setFormatter(MAIN_FORMATTER)

ERR_FILE = handlers.TimedRotatingFileHandler(
    ERR_PATH,
    encoding=ENCODING,
    interval=1,
    when="D",
)
ERR_FILE.setFormatter(MAIN_FORMATTER)
ERR_FILE.setLevel(logging.ERROR)

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger("logger")
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.addHandler(ERR_FILE)
LOGGER.setLevel(LOGGING_LEVEL)


# отладка
if __name__ == "__main__":
    LOGGER.critical("Критическая ошибка")
    LOGGER.error("Ошибка")
    LOGGER.debug("Отладочная информация")
    LOGGER.info("Информационное сообщение")
