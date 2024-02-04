from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class PaginationDungeon(CallbackData, prefix="dungeon"):
    action: str

class PaginationRbf(CallbackData, prefix="bf"):
    action: str

class PaginationAction(CallbackData, prefix="act_pl"):
    action: str

class PaginationChoose(CallbackData, prefix="two"):
    action: str

class Pagination(CallbackData, prefix="pag"):
    action: str


def paginator(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Лиса", callback_data=Pagination(action="fox", page=page).pack()),
        InlineKeyboardButton(text="Олень", callback_data=Pagination(action="deer", page=page).pack()),
        InlineKeyboardButton(text="Кот", callback_data=Pagination(action="cat", page=page).pack()),
        InlineKeyboardButton(text="Подтвердить", callback_data=Pagination(action="accept", page=page).pack()),
        width=3
    )
    return builder.as_markup()

def paginator_choose(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Лунария Старгейзер", callback_data=PaginationChoose(action="lunaria", page=page).pack()),
        InlineKeyboardButton(text="Шейд Шифтвульф", callback_data=PaginationChoose(action="sheid", page=page).pack()),
        InlineKeyboardButton(text="Леонард Ноктюрн", callback_data=PaginationChoose(action="bat", page=page).pack()),
        InlineKeyboardButton(text="Говорить с персонажем", callback_data=PaginationChoose(action="accept", page=page).pack()),
        # InlineKeyboardButton(text="Кот", callback_data=Pagination(action="cat", page=page).pack()),
        # InlineKeyboardButton(text="Подтвердить", callback_data=Pagination(action="accept", page=page).pack()),
        width=2
    )
    return builder.as_markup()

def paginator_action_ch(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Говорить", callback_data=PaginationAction(action="talk", page=page).pack()),
        InlineKeyboardButton(text="Сделать подарок", callback_data=PaginationAction(action="gift", page=page).pack()),
        InlineKeyboardButton(text="Флиртовать", callback_data=PaginationAction(action="flirt", page=page).pack()),
        InlineKeyboardButton(text="Предложить руку и сердце", callback_data=PaginationAction(action="bestfriend", page=page).pack()),
        InlineKeyboardButton(text="Расстаться с персонажем", callback_data=PaginationAction(action="bestfriend_not", page=page).pack()),
        # InlineKeyboardButton(text="Подтвердить", callback_data=Pagination(action="accept", page=page).pack()),
        width=2
    )
    return builder.as_markup()

def paginator_dungeon(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Двигаться дальше", callback_data=PaginationDungeon(action="next", page=page).pack()),
        InlineKeyboardButton(text="Атакавать", callback_data=PaginationDungeon(action="atack", page=page).pack()),
        InlineKeyboardButton(text="Лечиться", callback_data=PaginationDungeon(action="heal", page=page).pack()),
        InlineKeyboardButton(text="Покинуть подземелье", callback_data=PaginationDungeon(action="leave", page=page).pack()),
        # InlineKeyboardButton(text="Подтвердить", callback_data=Pagination(action="accept", page=page).pack()),
        width=2
    )
    return builder.as_markup()

def paginator_remove_bf(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Подтвердить", callback_data=PaginationRbf(action="accept", page=page).pack()),
        InlineKeyboardButton(text="Отменить", callback_data=PaginationRbf(action="cancel", page=page).pack()),
        width=2
    )
    return builder.as_markup()