![Lint](https://github.com/zzzkorn/progress-proxylogger/actions/workflows/lint.yml/badge.svg)

# Proxy сервер с возможностью логирования данных

|         Ресурс | Адресс                  | Ссылка                       |
| -------------: | ----------------------- | ---------------------------- |
|           geos | 46.150.163.148 : 50101  |                              |
|        gpshome | 185.60.134.234 : 50101  | https://map.gpshome.ru/main/ |
|         wialon | 213.219.245.116 : 20100 |
|            amt | 1.1.1.1 : 1             |
|      aoglonass | 82.116.45.252 : 3888    |
|     aoglonass2 | 193.232.47.4 : 40005    |
| n_egts_servers | 185.137.233.176:18900   |

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

```bash
python main.py -t imitation
```

## Запуск декодера пакетов с сырыми данными

```bash
python main.py -t decode
```
