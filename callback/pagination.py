from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from keyboards import fabric, reply
import sqlite3
import aiofiles
from aiogram.types import InputFile
import os
from aiogram import types
router = Router()
@router.callback_query(fabric.Pagination.filter(F.action.in_(["fox", "deer", "cat", "accept"])))
async def pagination_handler( call: CallbackQuery, callback_data: fabric.Pagination):
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
    result = cur.fetchone()
    if result == None:
        await call.message.answer(f"Отправьте мне 'Начать игру'", reply_markup=reply.main)
    else:
        if result[2] != 0:
            if result[4] != 'true':
                if callback_data.action == "fox":
                    cur.execute("UPDATE users SET rase = ? WHERE name = ?", ('лиса', call.from_user.id,))
                    path_img = "image/fox.jpg"
                    await call.message.reply_photo(photo=types.FSInputFile(path=path_img), caption="Ваша раса была установлена как Лиса.")
                    await call.answer(f"Ваш персонаж установлен как Лис 🦊")
                    db.commit()
                elif callback_data.action == "deer":
                    cur.execute("UPDATE users SET rase = ? WHERE name = ?", ('олень', call.from_user.id,))
                    path_img = "image/deer.jpg"
                    await call.message.reply_photo(photo=types.FSInputFile(path=path_img), caption="Ваша раса была установлена как Олень.")
                    await call.answer(f"Ваш персонаж установлен как Олень 🦌")
                    db.commit()
                elif callback_data.action == "cat":
                    cur.execute("UPDATE users SET rase = ? WHERE name = ?", ('кот', call.from_user.id,))
                    path_img = "image/cat.jpg"
                    await call.message.reply_photo(photo=types.FSInputFile(path=path_img), caption="Ваша раса была установлена как Кот.")
                    await call.answer(f"Ваш персонаж установлен как Кот 🐱")
                    db.commit()
                elif callback_data.action == "accept":
                    if result[3] != 'ничего':
                        if result[4] == 'false':
                            cur.execute("UPDATE users SET is_race_choose = ? WHERE name = ?", ('true', call.from_user.id,))
                            await call.message.answer(f"Вы успешно подтвердили своего персонажа: {result[3]} 🐾")
                            db.commit()
                    else:
                        await call.message.answer(f"Выберите персонажа.")
            else:
                await call.message.answer(f"Вы уже выбрали своего персонажа: {result[3]} 🐾")
        else:
            await call.message.answer(f"Вы не начали игру.")
    db.close()
    await call.answer()