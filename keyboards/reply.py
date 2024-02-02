from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Начать игру"),
            KeyboardButton(text="Меню игры")
        ],
        [
            KeyboardButton(text="О боте"),
            KeyboardButton(text="Спец. кнопки")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбирите действие из меню",
    selective=True
)
game = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Выбрать персонажа"),
            KeyboardButton(text="Кто рядом"),
            KeyboardButton(text="Спустится в подземелье")
            
        ],
        [
            KeyboardButton(text="Статистика")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)