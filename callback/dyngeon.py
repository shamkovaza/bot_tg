from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from keyboards import fabric, reply
import sqlite3
import aiofiles
from aiogram.types import InputFile
import os
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress
import random
router = Router()
@router.callback_query(fabric.PaginationDungeon.filter(F.action.in_(["next", "atack", "heal", "leave"])))
async def paginator_dungeon( call: CallbackQuery, callback_data: fabric.PaginationDungeon):
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (call.from_user.id,))
    result = cur.fetchone()
    cur_event = db.cursor()
    cur_safe = db.cursor()
    cur_safe.execute("SELECT * FROM dungeon_safe WHERE name = ?", (call.from_user.id,))
    result_safe = cur_safe.fetchone()
    if result == None:
        await call.message.answer(f"Отправьте мне 'Начать игру'", reply_markup=reply.main)
    else:
        if result_safe == None:
            cur_safe.execute("INSERT INTO dungeon_safe (name, heal, record, battle_npc, battle_npc_heal) VALUES (?, ?, ?, ?, ?)", (call.from_user.id, 100, 0, '', 0))
            db.commit()
        else:
            if result[4] != 'false':
                if callback_data.action == "next":
                    if result_safe[5] <= 0:
                        if result_safe[2] >= 1:
                            battle = random.randint(0, 1)
                            if battle == 1:
                                cur.execute("SELECT * FROM info_battle_npc WHERE id = ?", (random.randint(1, 6),))
                                res_npcfor_btl = cur.fetchone()
                                with suppress(TelegramBadRequest):
                                    await call.message.edit_text(
                                        f"На вашем пути появился {res_npcfor_btl[1]}.\n <b>{res_npcfor_btl[2]}</b>",
                                        reply_markup=fabric.paginator_dungeon()
                                    ) 
                                heal_btl_npc = random.randint(40, 100)
                                cur_safe.execute("UPDATE dungeon_safe SET battle_npc = ?, battle_npc_heal = ? WHERE name = ?", (res_npcfor_btl[1], heal_btl_npc, call.from_user.id,))
                                db.commit()
                            else:
                                cur_event.execute("SELECT * FROM dungeon_event WHERE id = ?", (random.randint(1, 2),))
                                result_event = cur_event.fetchone()
                                random_ = random.randint(1, min(3, len(result_event)-1))
                                event = result_event[random_].split('; ')
                                _heal_false = result_safe[2]
                                if event[0] == 'false':
                                    _heal_info = random.randint(1, 70)
                                    _heal_false_up = _heal_false - _heal_info
                                    cur_safe.execute("UPDATE dungeon_safe SET heal = ? WHERE name = ?", (_heal_false_up, call.from_user.id,))
                                    db.commit()
                                    cur_safe.execute("SELECT * FROM dungeon_safe WHERE name = ?", (call.from_user.id,))
                                    result_safe = cur_safe.fetchone()
                                    with suppress(TelegramBadRequest):
                                        await call.message.edit_text(
                                            f"{event[1]} \n Вы потеряли {_heal_info} \n Ваш уровень здоровья {result_safe[2]}",
                                            reply_markup=fabric.paginator_dungeon()
                                        ) 
                                else:
                                    items_event = random.randint(1, 2)
                                    if items_event == 1:
                                        with suppress(TelegramBadRequest):
                                            await call.message.edit_text(
                                                f"{event[1]} \n Вы нашли немного лечебных ягод",
                                                reply_markup=fabric.paginator_dungeon()
                                            ) 
                                        cur.execute("SELECT items FROM users WHERE name = ?", (call.from_user.id,))
                                        res_item = cur.fetchone()
                                        res_item = list(res_item)
                                        res_item.append('Лечебные ягоды')
                                        res_item = tuple(res_item)
                                        res_item_str = ", ".join(res_item)
                                        cur_safe.execute("UPDATE users SET items = ? WHERE name = ?", (res_item_str, call.from_user.id,))
                                        db.commit()
                                    if items_event == 2:
                                        rand_item_for = ['Лунный камень', 'Лесной сапфир', 'Корни жизни']
                                        random_element = random.choice(rand_item_for)
                                        with suppress(TelegramBadRequest):
                                            await call.message.edit_text(
                                                f"{event[1]} \n Вы нашли {random_element}",
                                                reply_markup=fabric.paginator_dungeon()
                                            ) 
                                        cur.execute("SELECT items FROM users WHERE name = ?", (call.from_user.id,))
                                        res_item = cur.fetchone()
                                        res_item = list(res_item)
                                        res_item.append(random_element)
                                        res_item = tuple(res_item)
                                        res_item_str = ", ".join(res_item)
                                        cur_safe.execute("UPDATE users SET items = ? WHERE name = ?", (res_item_str, call.from_user.id,))
                                        db.commit()
                        else:
                            with suppress(TelegramBadRequest):
                                await call.message.edit_text(
                                    f"Не хватает здоровья, уровень здоровье: {result_safe[2]}",
                                    reply_markup=fabric.paginator_dungeon()
                                )
                    else:
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"На вашем пути стоит {result_safe[4]}, у вас нет выбора как атаковать его.",
                                reply_markup=fabric.paginator_dungeon()
                            )
                if callback_data.action == "atack":
                    if result_safe[5] >= 1:
                        if result_safe[2] >= 1:
                            down_hp_heroy = random.randint(1, 30)
                            down_hp_npc = random.randint(5, 45)
                            u_heah = result_safe[2] - down_hp_heroy
                            u_npc_heal = result_safe[5] - down_hp_npc 
                            with suppress(TelegramBadRequest):
                                await call.message.edit_text(
                                    f"Вы атакуете {result_safe[4]} и наносите ему урон в размере {down_hp_npc}.\n Но получаете {down_hp_heroy} урона. \n Ваш уровень здоровья равен: {result_safe[2]}.",
                                    reply_markup=fabric.paginator_dungeon()
                                )   
                            cur_safe.execute("UPDATE dungeon_safe SET heal = ?, battle_npc_heal = ? WHERE name = ?", (u_heah, u_npc_heal, call.from_user.id,))
                            db.commit()
                        else:
                            with suppress(TelegramBadRequest):
                                await call.message.edit_text(
                                    f"Не хватает здоровья, уровень здоровье: {result_safe[2]}",
                                    reply_markup=fabric.paginator_dungeon()
                                )
                    else:
                        cur_safe.execute("UPDATE dungeon_safe SET battle_npc = ? WHERE name = ?", ('', call.from_user.id,))
                        db.commit()
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"Пока что некого атаковать.",
                                reply_markup=fabric.paginator_dungeon()
                            )     
                if callback_data.action == "heal":
                    cur.execute("SELECT items FROM users WHERE name = ?", (call.from_user.id,))
                    res_item = cur.fetchone()
                    item = res_item[0].split(', ')
                    if "Лечебные ягоды" in item:
                        r_heal = random.randint(10, 35)
                        up_heal = r_heal + result_safe[2]
                        cur_safe.execute("UPDATE dungeon_safe SET heal = ? WHERE name = ?", (up_heal, call.from_user.id,))
                        item.remove('Лечебные ягоды')
                        cur.execute("UPDATE users SET items = ? WHERE name = ?", (', '.join(item), call.from_user.id,))
                        db.commit()
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"Вы восстановили {r_heal} здоровья.\n Ваш уровень здоровья составляет: {result_safe[2]}",
                                reply_markup=fabric.paginator_dungeon()
                            )
                    else:
                        r_heal = random.randint(1, 5)
                        up_heal = r_heal + result_safe[2]
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"У вас нет лечащего предмета, но вы будете лечиться только не так быстро. \n Вы восстановили: {r_heal}",
                                reply_markup=fabric.paginator_dungeon()
                            )
                        cur_safe.execute("UPDATE dungeon_safe SET heal = ? WHERE name = ?", (up_heal, call.from_user.id,))
                        db.commit()
                if callback_data.action == "leave":
                    with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"Выход.",
                                reply_markup=fabric.paginator_choose()
                            )
            else:   
                await call.message.answer(f"Подтвердите персонажа")
    db.close()
    await call.answer()