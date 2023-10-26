from aiogram.dispatcher.filters.state import StatesGroup, State


class Comment(StatesGroup):
    input_code = State()
    input_video = State()


class Manual(StatesGroup):
    manual_done = State()


class Organ(StatesGroup):
    chan = State()


class Market(StatesGroup):
    media = State()


class Selections(StatesGroup):
    lan = State()


class Welcome(StatesGroup):
    wel = State()
