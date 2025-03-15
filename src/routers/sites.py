import os
from typing import Iterable, Any
import logging

from aiogram import Router, F, types, Bot
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from src.config import Settings
from src.core.db import Database
from src.keyboards import Keyboards
from src.states import AddSource
from src.utils import parse_excel
from src.core import database as db
from src.models import Sources

router = Router(name="Sites router")
settings = Settings()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def handle_start_message(msg: types.Message) -> None:
    await msg.answer(
        text="Привет, данный бот предназначен для добавления новых сайтов в базу для парсинга.",
        reply_markup=Keyboards.MAIN_MENU,
    )


@router.message(StateFilter(None), F.text == "Загрузить файл")
async def handle_action_upload_file(
        msg: types.Message,
        state: FSMContext,
) -> None:
    await msg.answer(
        text="Загрузите файл формата Excel...",
        reply_markup=Keyboards.UPLOAD_FILE_MENU,
    )
    await state.set_state(AddSource.wait_for_file)


@router.message(AddSource.wait_for_file, F.text == "Отмена")
async def handle_action_cancel(msg: types.Message, state: FSMContext) -> None:
    await msg.reply(
        text="Загрузка файла отменена!",
        reply_markup=Keyboards.MAIN_MENU,
    )
    await state.set_state(None)


async def save_file_from_user(user_msg: types.Message) -> str:
    file_id = user_msg.document.file_id
    file_name = user_msg.document.file_name
    temp_bot = Bot(settings.BOT_TOKEN)
    file = await temp_bot.get_file(file_id)
    downloaded_file = await temp_bot.download_file(file.file_path)

    with open(file_name, 'wb') as f:
        f.write(downloaded_file.getvalue())

    return file_name


async def insert_sources(
        objects: Iterable[dict[str, Any]],
        database: Database,
) -> None:
    async with database.create_async_session() as session:
        session.add_all([Sources(**obj) for obj in objects])
        await session.commit()


@router.message(AddSource.wait_for_file, F.content_type == ContentType.DOCUMENT)
async def handle_file(msg: types.Message, state: FSMContext) -> None:
    file_name = await save_file_from_user(msg)
    source_dicts = []
    try:
        for record in parse_excel(file_name):
            source_dict = dict(
                title=record[0],
                url=record[1],
                xpath=record[2],
            )
            source_dicts.append(source_dict)

        await insert_sources(
            objects=source_dicts,
            database=db,
        )

    except Exception as e:
        logger.debug("Error while reading table: %s", str(e))
        await msg.answer(
            text="В процессе чтения файла произошла ошибка. Убедитесь в корректности таблицы и повторите снова.",
            reply_markup=Keyboards.UPLOAD_FILE_MENU,
        )
        await state.set_state(AddSource.wait_for_file)
        return
    finally:
        os.remove(file_name)

    success_answer_text = "Источники успешно добавлены:\n\n"
    for source_dict in source_dicts:
        pretty_source = "\n".join([f"{k}: {v}" for k, v in source_dict.items()])
        success_answer_text += pretty_source + "\n\n"

    await msg.answer(
        text=success_answer_text,
        reply_markup=Keyboards.MAIN_MENU,
    )

    await state.set_state(None)


@router.message(AddSource.wait_for_file, F.text)
async def handle_text_while_waiting_file(msg: types.Message) -> None:
    await msg.reply(
        text="Пожалуйста, загрузите файл формата excel...",
        reply_markup=Keyboards.UPLOAD_FILE_MENU,
    )


@router.message(F.text)
async def handle_others(msg: types.Message, state: FSMContext) -> None:
    reset_kb_msg = await msg.answer(
        text="Контекст потерян или отсутствует. Возвращаюсь в главное меню...",
        reply_markup=Keyboards.MAIN_MENU,
    )
    await state.set_state(None)
