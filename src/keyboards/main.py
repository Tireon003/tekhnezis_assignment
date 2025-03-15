from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Keyboards:

    MAIN_MENU = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Загрузить файл")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
    )

    UPLOAD_FILE_MENU = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Ожидается excel файл",
    )
