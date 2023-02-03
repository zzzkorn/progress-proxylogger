![Lint](https://github.com/zzzkorn/progress-proxylogger/actions/workflows/lint.yml/badge.svg)

# Proxy сервер EGTS с возможностью логирования данных

|     Ресурс | Адресс                  | Ссылка                           |
| ---------: | ----------------------- | -------------------------------- |
|    gpshome | 213.219.245.116 : 20100 | https://map.gpshome.ru/main/     |
| aoglonass2 | 193.232.47.4 : 40005    | https://monitoring.aoglonass.ru/ |

# Краткая информация о модуле

```bash
python main.py -h
```

## Запуск прокси сервера

```bash
python main.py
```

или

```bash
python main.py -t proxy
```

## Запуск имитатора

Имитатор необходимо запускать только после запуска прокси сервера

### Имитация работы клиентов

```bash
python main.py -t client_imitation
```

### Полная имитация

```bash
python main.py -t full_imitation
```

## Запуск декодера пакетов с сырыми данными

```bash
python main.py -t decode
```

# Аргументы конфигурационного файла

```python
# Логирование данных в объект logger
FILE_LOG = TRUE
```

```python
# Информация для подключения к БД
DATABASE_ENGINE = postgres://user:password@db.example.com:5432/production_db?client_encoding=utf8
```

```python
# Адресс на котором будет развернут proxy сервер
ADDRESS = 192.193.0.1: 16000
```

```python
# Адресс для удаленного подключения
REMOTE = 192.1.10.1: 20100
```

```python
# Время (в секундах) после последнкго получеого TCP пакета после которого будет сбрасываться TCP сессия
SOCKET_TIMEOUT = 15.4
```

```python
# Максимальное количество клиентов, подклюбчаемых к proxy-серверу (так же используется в имитаторе, чтобы определить количество одновременно открытых клиентов)
MAX_CONNECTIONS = 4
```

```python
# Максимальная длинна пакета
MAX_PACKAGE_LENGTH = 8192
```

```python
# Список IMEI ID, которые используются при имитации взаимодействия. При этом количество открытых клиентов выбирается как min(len(IMITATION_IMEI_IDS), MAX_CONNECTIONS)
IMITATION_IMEI_IDS = 1111111, 2222222, 333333333
```

```python
# Задержка между отправкой пакетов клиентами при имитации сетевого взаимодействия
IMITATION_DELAY = 1
```
