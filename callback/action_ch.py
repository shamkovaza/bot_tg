from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from keyboards import fabric, reply
import sqlite3
from aiogram.types import InputFile
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
import random
import asyncio
router = Router()
@router.callback_query(fabric.PaginationAction.filter(F.action.in_(["talk", "gift"])))
async def pagination_handler( call: CallbackQuery, callback_data: fabric.PaginationAction):
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
    result = cur.fetchone()
    cur_npc = db.cursor()
    cur_npc.execute("SELECT * FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, result[6]))
    result_npc = cur_npc.fetchone()
    if result == None:
        await call.message.answer(f"Отправьте мне 'Начать игру'", reply_markup=reply.main)
    else:
        if callback_data.action == "talk":
            if result_npc == None or result_npc[2] == None:
                cur_npc.execute("INSERT INTO action_player_npc (name, name_npc) VALUES (?, ?)", (call.from_user.id, result[6]))
                db.commit()
            else:
                if result[7] == 'true':
                    cur_dialog_npc = db.cursor()
                    cur_dialog_npc.execute("SELECT * FROM npc WHERE name = ?", (result[6],))
                    result_dualog = cur_dialog_npc.fetchone()
                    if result_npc[3] <= 5:
                        random_number = random.randint(6, 7)        
                    else:
                        random_number = random.randint(3, 5)
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"{result_dualog[random_number]}",
                            reply_markup=fabric.paginator_action_ch()
                        )
                else:
                    await call.message.answer(f"Подтвердите персонажа к которому хотите подойти", reply_markup=reply.game) 
        elif callback_data.action == "gift":
            rand_item_for = ['Лунный камень', 'Лесной сапфир', 'Корни жизни']
            random_element = random.choice(rand_item_for)
            print(result_npc[1])
            if result_npc[4] == None or result_npc[4] == '':
                print("nones")
                cur_npc.execute("UPDATE action_player_npc SET item = ? WHERE name = ? AND name_npc = ?", (random_element, call.from_user.id, result[6],))
                db.commit()
                cur_npc.execute("SELECT * FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, result[6]))
                result_npc = cur_npc.fetchone()
            if result[8] != 'ничего':
                cur.execute("SELECT items FROM users WHERE name = ?", (call.from_user.id,))
                result_item = cur.fetchone()
                item = result_item[0].split(', ')
                if result_npc[4] in item:
                    cur_npc.execute("SELECT * FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, result[6]))
                    result_npc = cur_npc.fetchone()
                    mood_r = random.randint(1, 10)
                    mood = result_npc[3] + mood_r
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"Вы подарили персонажу {result_npc[2]} {result_npc[4]} и получили {mood_r} доверия.",
                                reply_markup=fabric.paginator_action_ch()
                            ) 
                    cur_npc.execute("UPDATE action_player_npc SET item = ?, mood = ? WHERE name = ? AND name_npc = ?", ('', mood, call.from_user.id, result[6],))
                    item.remove(result_npc[4])
                    cur.execute("UPDATE users SET items = ? WHERE name = ?", (', '.join(item), call.from_user.id,))
                    db.commit()
                else:
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"У вас нет предмета {result_npc[4]} который хочет {result_npc[2]}",
                                reply_markup=fabric.paginator_action_ch()
                            ) 
            else:
                with suppress(TelegramBadRequest):
                    await call.message.edit_text(
                        f"Персонаж {result_npc[2]} хочет чтобы вы достали {result_npc[4]} \n В вашем инвенторе нет никаких предметов",
                            reply_markup=fabric.paginator_action_ch()
                        ) 
    db.close()
    await call.answer()