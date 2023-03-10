# flake8: noqa: E402
import logging

# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 8192
# БД
DATABASE_ENGINE = "sqlite:///test_base.db3"
# Кодировка проекта
ENCODING = "utf-8"
# Логировапние в файл
FILE_LOG = True
# Задержка отправки пакетов имитатора
IMITATION_DELAY = 5
# Время ожидания сокетом принятого пакета
SOCKET_TIMEOUT = 200
TEST_SERVER_PORT = 40000

# ID устройст для имитации
IMITATION_IMEI_IDS = "358887095658464, 358887095658564, 358887095658664"
