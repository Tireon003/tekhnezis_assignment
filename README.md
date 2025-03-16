# Тестовое задание от ТЕХНЕЗИС
Добавление новых источников для парсинга реализовано через Тг-бота.

*Проект разработан на Python 3.12

### Как развернуть?

1. Клонируем репозиторий:
```shell
git clone https://github.com/Tireon003/tekhnezis_assignment.git
```
2. Переходим в папку с проектом. Устанавливаем и активируем виртуальное окружение:
```shell
python -m venv venv
./venv/Scripts/activate
```
3. Создаем в корневой папке проекта .env файл с содержимым:
```text
BOT_TOKEN="токен_тг_бота"  ; вставляет валидный токен бота Tg
LOG_LEVEL="INFO"  ; Устанавливаем желаемый уровень логирования (DEBUG, INFO, WARNING, ERROR)
LOG_FORMAT="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)-7s - %(message)s"
```
4. Запускаем проект:
```shell
python src/main.py 
```
5. Готово!
