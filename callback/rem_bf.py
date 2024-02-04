from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from keyboards import fabric, reply
import sqlite3
from aiogram.types import InputFile
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
router = Router()
@router.callback_query(fabric.PaginationRbf.filter(F.action.in_(["accept", "cancel"])))
async def pagination_handler( call: CallbackQuery, callback_data: fabric.PaginationRbf):
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
    result = cur.fetchone()
    if result == None:
        await call.message.answer(f"Отправьте мне 'Начать игру'", reply_markup=reply.main)
    else:
        if result[2] != 0:
            if callback_data.action == "accept":
                cur.execute("SELECT relationship, relationship_npc FROM users WHERE name = ?", (call.from_user.id,))
                result = cur.fetchone()
                if result[0] != 'false':
                    cur.execute("UPDATE action_player_npc SET mood = ?, love = ? WHERE name = ? AND name_npc = ?", (-15, 0, call.from_user.id, result[1],))
                    cur.execute("UPDATE users SET relationship = ?, relationship_npc = ? WHERE name = ?", ('false', 'false', call.from_user.id,))
                    db.commit()
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"Вы расстались с персонажем {result[1]}",
                            reply_markup=fabric.paginator_action_ch()
                        )
                else:
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"Вы не в отношениях.",
                            reply_markup=fabric.paginator_action_ch()
                        )
            if callback_data.action == "cancel":
                with suppress(TelegramBadRequest):
                    await call.message.edit_text(
                        f"Вы передумали",
                        reply_markup=fabric.paginator_action_ch()
                    )
        else:
            await call.message.answer(f"Вы не начали игру.")
    db.close()
    await call.answer()