![Lint](https://github.com/zzzkorn/progress-proxylogger/actions/workflows/lint.yml/badge.svg)

# Proxy сервер с возможностью логирования данных

|     Ресурс | Адресс                  | Ссылка                           |
| ---------: | ----------------------- | -------------------------------- |
|    gpshome | 213.219.245.116 : 20100 | https://map.gpshome.ru/main/     |
| aoglonass2 | 193.232.47.4 : 40005    | https://monitoring.aoglonass.ru/ |

## Краткая информация о модуле

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
