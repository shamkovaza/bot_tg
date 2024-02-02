from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from keyboards import fabric, reply
import sqlite3
from aiogram.types import InputFile
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
from aiogram import types
router = Router()
@router.callback_query(fabric.PaginationChoose.filter(F.action.in_(["lunaria", "sheid", "bat", "accept"])))
async def pagination_choose( call: CallbackQuery, callback_data: fabric.PaginationChoose):
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    npc_cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
    result = cur.fetchone()
    if result == None:
        await call.message.answer(f"Отправьте мне 'Начать игру'", reply_markup=reply.main)
    else:
        if callback_data.action == "lunaria":
            npc_cur.execute("SELECT * FROM npc WHERE name = ?", ('Лунария Старгейзер',))
            result_npc = npc_cur.fetchone()
            with suppress(TelegramBadRequest):
                await call.message.edit_text(
                    f"Вы думаете подойти к персонажу с именем {result_npc[0]} \n {result_npc[1]}",
                    reply_markup=fabric.paginator_choose()
                )
            cur.execute("UPDATE users SET choose_npc = ?, choose_npc_is = ? WHERE name = ?", (result_npc[0], 'false', call.from_user.id,))
            db.commit()
            db.close()
        elif callback_data.action == "sheid":
            npc_cur.execute("SELECT * FROM npc WHERE name = ?", ('Шейд Шифтвульф',))
            result_npc = npc_cur.fetchone()
            with suppress(TelegramBadRequest):
                await call.message.edit_text(
                    f"Вы думаете подойти к персонажу с именем {result_npc[0]} \n {result_npc[1]}",
                    reply_markup=fabric.paginator_choose()
                )
            cur.execute("UPDATE users SET choose_npc = ?, choose_npc_is = ? WHERE name = ?", (result_npc[0], 'false', call.from_user.id,))
            db.commit()
            db.close()
        elif callback_data.action == "bat":
            npc_cur.execute("SELECT * FROM npc WHERE name = ?", ('Леонард Ноктюрн',))
            result_npc = npc_cur.fetchone()
            with suppress(TelegramBadRequest):
                await call.message.edit_text(
                    f"Вы думаете подойти к персонажу с именем {result_npc[0]} \n {result_npc[1]}",
                    reply_markup=fabric.paginator_choose()
                )
            cur.execute("UPDATE users SET choose_npc = ?, choose_npc_is = ? WHERE name = ?", (result_npc[0], 'false', call.from_user.id,))
            db.commit()
            db.close()
        elif callback_data.action == "accept":
            await call.message.answer(f"Вы подходите к персонажу {result[6]}", reply_markup=fabric.paginator_action_ch())
            cur.execute("UPDATE users SET choose_npc_is = ? WHERE name = ?", ('true', call.from_user.id,))
            db.commit()
    db.close()
    await call.answer()