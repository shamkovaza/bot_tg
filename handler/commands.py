import logging
import asyncio
from contextlib import suppress
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
import random
from aiogram.exceptions import TelegramBadRequest
from keyboards import reply
from aiogram import Router

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Приветствую тебя, <b>{message.from_user.first_name}</b>", reply_markup=reply.main)
