from aiogram.fsm.state import StatesGroup, State


class AddSource(StatesGroup):
    wait_for_file = State()
