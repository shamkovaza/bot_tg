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
@router.callback_query(fabric.PaginationAction.filter(F.action.in_(["talk", "gift", "flirt", "bestfriend", "bestfriend_not"])))
async def pagination_handler( call: CallbackQuery, callback_data: fabric.PaginationAction):
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
    result = cur.fetchone()
    cur_npc = db.cursor()
    cur_npc.execute("SELECT * FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, result[6]))
    result_npc = cur_npc.fetchone()
    if result == None or result[6] == 'false':
        await call.message.answer(f"Отправьте мне 'Начать игру'", reply_markup=reply.main)
    else:
        if callback_data.action == "talk":
            if result_npc == None or result_npc[2] == None:
                if result[6] != 'false':
                    cur_npc.execute("INSERT INTO action_player_npc (name, name_npc) VALUES (?, ?)", (call.from_user.id, result[6]))
                    db.commit()
                    cur_dialog_npc = db.cursor()
                    cur_dialog_npc.execute("SELECT * FROM npc WHERE name = ?", (result[6],))
                    result_dualog = cur_dialog_npc.fetchone()
                    cur_npc.execute("SELECT * FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, result[6]))
                    result_npc = cur_npc.fetchone()
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
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"Выберите персонажа с которым хотите говорить.",
                            reply_markup=fabric.paginator_action_ch()
                        )
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
        
        if callback_data.action == "flirt":
            cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
            result = cur.fetchone()
            if result[6] != 'false' and result[7] != 'false':
                cur.execute("SELECT * FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, result[6],))
                result_act = cur.fetchone()
                if result_act is not None:
                    if result[6] != 'false' and result[7] != 'false':
                        cur_npc = db.cursor()
                        cur_npc.execute("SELECT * FROM npc WHERE name = ?", (result[6],))
                        result_npc = cur_npc.fetchone()
                        if result_act[3] >= 65:
                            r_love = random.randint(1, 5)
                            u_love = result_act[5] + r_love
                            mood_r = random.randint(1, 15) 
                            mood = result_act[3] - mood_r
                            cur.execute("UPDATE action_player_npc SET love = ?, mood = ? WHERE name = ? AND name_npc = ?", (u_love, mood, call.from_user.id, result[6],))
                            db.commit()
                            is_flirt = random.randint(8, 10)
                            with suppress(TelegramBadRequest):
                                await call.message.edit_text(
                                    f"{result_npc[is_flirt]}",
                                    reply_markup=fabric.paginator_action_ch()
                                )
                        else:
                            cur.execute("SELECT * FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, result[6],))
                            result_act = cur.fetchone()
                            if result_act[3] >= 3:
                                r_love = random.randint(1, 5)
                                u_love = result_act[5] - r_love
                                mood_r = random.randint(1, 30) 
                                mood = result_act[3] - mood_r
                                cur.execute("UPDATE action_player_npc SET love = ?, mood = ? WHERE name = ? AND name_npc = ?", (u_love, mood, call.from_user.id, result[6],))
                                db.commit()
                                is_flirt = random.randint(11, 12)
                                with suppress(TelegramBadRequest):
                                    await call.message.edit_text(
                                        f"{result_npc[is_flirt]} \n Потеряли {mood_r} доверия. \n Сейчас оно составляет: {mood} \n Подсказка: Повышайте свой уровень доверия для этого.",
                                        reply_markup=fabric.paginator_action_ch()
                                    )
                            else:
                                is_flirt = random.randint(11, 12)
                                with suppress(TelegramBadRequest):
                                    await call.message.edit_text(
                                        f"{result_npc[is_flirt]}",
                                        reply_markup=fabric.paginator_action_ch()
                                    )
                    else:
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"Подойдите к персонажу и начните с ним диалог.",
                                reply_markup=fabric.paginator_action_ch()
                            )
                else:
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"Поговорите с персонажем.",
                            reply_markup=fabric.paginator_action_ch()
                        )
            else:
                with suppress(TelegramBadRequest):
                    await call.message.edit_text(
                        f"Подойдите к персонажу и начните с ним диалог.",
                        reply_markup=fabric.paginator_action_ch()
                    )
        if callback_data.action == "bestfriend":
            cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
            result = cur.fetchone()
            if result[6] != 'false' and result[7] != 'false':
                cur.execute("SELECT * FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, result[6],))
                result_act = cur.fetchone()
                cur.execute("SELECT relationship FROM users WHERE name = ?", (call.from_user.id,))
                relationsh = cur.fetchone()
                if result_act is not None:
                    if result_act[5] >= 80:
                        if relationsh[0] == 'false':
                            list = ["rel1", "rel2", "rel3"]
                            random_element = random.choice(list)
                            query = f"SELECT {random_element} FROM npc WHERE name = ?"
                            cur.execute(query, (result[6],))
                            query_result = cur.fetchone()
                            with suppress(TelegramBadRequest):
                                await call.message.edit_text(
                                    f"{query_result[0]}",
                                    reply_markup=fabric.paginator_action_ch()
                                ) #10
                            cur_npc.execute("UPDATE users SET relationship = ?, relationship_npc = ? WHERE name = ?", ('true', result[6], call.from_user.id,))
                            db.commit()
                        else:
                            with suppress(TelegramBadRequest):
                                await call.message.edit_text(
                                    f"У вас уже есть романтическая связь с {result[10]}.",
                                    reply_markup=fabric.paginator_action_ch()
                                ) #10
                    else:
                        print(relationsh[0], result_act[5])
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"Недостаточно романтической связи с этим персонажем.",
                                reply_markup=fabric.paginator_action_ch()
                            )
                else:
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"Поговорите с персонажем.",
                            reply_markup=fabric.paginator_action_ch()
                        )
            else:
                with suppress(TelegramBadRequest):
                    await call.message.edit_text(
                        f"Подойдите к персонажу и начните с ним диалог.",
                        reply_markup=fabric.paginator_action_ch()
                    )
        elif callback_data.action == "gift":
            rand_item_for = ['Лунный камень', 'Лесной сапфир', 'Корни жизни']
            random_element = random.choice(rand_item_for)
            if result_npc is not None:
                if result_npc[4] is None or result_npc[4] == '':
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
                                f"Вы подарили персонажу {result_npc[2]} {result_npc[4]} и получили {mood_r} доверия.\n Доверия к этому персонажу составляет {mood}",
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
            else:
                with suppress(TelegramBadRequest):
                    await call.message.edit_text(
                        f"Поговорите с персонажем.",
                        reply_markup=fabric.paginator_action_ch()
                    )
        elif callback_data.action == "bestfriend_not":
            if result_npc is not None:
                cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
                result = cur.fetchone()
                if result[6] != 'false' and result[7] != 'false':
                    cur.execute("SELECT relationship FROM users WHERE name = ?", (call.from_user.id,))
                    relationsh = cur.fetchone()
                    if relationsh[0] == 'true':
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"Вы уверены что хотите расстаться с персонажем {result[10]} ?",
                                    reply_markup=fabric.paginator_remove_bf()
                                ) 
                    else:
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"Вы не в отношениях.",
                                    reply_markup=fabric.paginator_action_ch()
                                ) 
                else:
                    with suppress(TelegramBadRequest):
                        await call.message.edit_text(
                            f"Выберите персонажа и начните с ним диалог.",
                                reply_markup=fabric.paginator_action_ch()
                            ) 
            else:
                with suppress(TelegramBadRequest):
                    await call.message.edit_text(
                        f"Поговорите с персонажем.",
                        reply_markup=fabric.paginator_action_ch()
                    )
    db.close()
    await call.answer()