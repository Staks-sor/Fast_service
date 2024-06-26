# Проект на FASTAPI для автосервиса

Этот проект представляет собой веб-приложение на основе FASTAPI для автосервиса. Здесь вы найдете функционал, который поможет автосервису эффективно управлять своей работой, взаимодействовать с клиентами и отслеживать выполнение заказов.

## Основные функции:
- Регистрация клиентов и автомобилей
- Управление заказами и расписанием работы
- Отслеживание статуса выполнения заказов
- Коммуникация с клиентами через уведомления и обратную связь

## Технологии, использованные в проекте:
- FASTAPI - быстрый веб-фреймворк для создания API
- Python - основной язык программирования
- HTML/CSS/JavaScript - для создания пользовательского интерфейса
- База данных (например, SQLite) для хранения данных

## Установка и запуск:
1. Клонируйте репозиторий:
   
   git clone https://github.com/Staks-sor/Fast_service.git
   
2. Установите зависимости:
   
   pip install -r requirements.txt
   
3. Запустите приложение:
   
   uvicorn main:app --reload

## Использование poetry для зависимостей
### Установка

**poetry** возможно установить двумя способами:

1.  C помощью пакетного менеджера pip
```
pip install poetry
```

2. скачать с оф. сайта и установить напрямую
(данная команда работает на macOS, linux, Windows(WSL))

``` bash
curl -sSL https://install.python-poetry.org | python3 - 
```
### Конфигурация

Всю информацию о конфигурации **poetry** можно найти на официальном [сайте](https://python-poetry.org/docs/configuration/). Здесь хочу лишь упомянуть настройку виртуального окружения.

Для того чтобы виртуальное окружение создавалось внутри текущей директории, а не где то в директории кэша необходимо установить флаг **virtualenvs.in-project**

```
poetry config virtalenvs.in-project true
```

### Запуск виртаульного окружения и установка зависимостей

Для запуска виртуального окружения используется команда 
```
poetry shell
```
а для выхода из него просто 

```
exit
```

---

Все зависимости фиксируются в файлах **poetry.lock** и **pyproject.toml**. Для того чтобы установить все указанные в этих файлах зависимости используется команда 

```
poetry install
```
В данном проекте зависимости разделены на группы (пока prod и dev). указанная выше команда установит лишь prod зависимости. Для установки всех зависимостей необходимо использовать команду 

```
poetry install --with dev
```
### Добавление новых зависимостей
Для добавления новой зависимости в **prod**:
```
poetry add [package-name]@[version]
```
Версия опциональна, если она не указана будет установлена последняя версия пакета

Например:
```
poetry add fastapi
```
---
Для добавления новых зависимостей в в группу **dev**:
```
poetry add pytest --group dev
```