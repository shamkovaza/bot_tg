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
import g4f
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
            with suppress(TelegramBadRequest):
                await call.message.edit_text(
                    f"Происходит подготовка данных подземелья, нажмите ещё раз кнопку.",
                    reply_markup=fabric.paginator_dungeon()
                ) 
        else:
            if result[4] != 'false':
                if callback_data.action == "next":
                    if result_safe[5] <= 0:
                        if result_safe[2] >= 1:
                            battle = random.randint(0, 2)
                            if battle == 2:
                                cur.execute("SELECT name FROM npc")
                                names = [name[0] for name in cur.fetchall()]
                                rand_npc_for = names
                                r_npc = random.choice(rand_npc_for)
                                cur.execute("SELECT mood FROM action_player_npc WHERE name = ? AND name_npc = ?", (call.from_user.id, r_npc,))
                                res_mood = cur.fetchone()
                                if res_mood is not None:
                                    random_dialog = random.randint(0, 1)
                                    if res_mood[0] >= 15:
                                        cur.execute("SELECT dialog_inDangeon_true FROM npc WHERE name = ?", (r_npc,))
                                        res_dialog_true = cur.fetchone()
                                        dialog = res_dialog_true[0].split('; ')
                                        _heal_ = result_safe[2] 
                                        _heal_up = random.randint(1, 35)
                                        _heal_update_up = _heal_ + _heal_up
                                        cur_safe.execute("UPDATE dungeon_safe SET heal = ? WHERE name = ?", (_heal_update_up, call.from_user.id,))
                                        db.commit()
                                        cur_safe.execute("SELECT heal FROM dungeon_safe WHERE name = ?", (call.from_user.id,))
                                        result_heal = cur_safe.fetchone()
                                        with suppress(TelegramBadRequest):
                                            await call.message.edit_text(
                                                f"{dialog[random_dialog]} \n Вы получили {_heal_up} здоровья \n Уровень здоровье: {result_heal[0]}",
                                                reply_markup=fabric.paginator_dungeon()
                                            ) 
                                    else:
                                        cur.execute("SELECT dialog_inDangeon_false FROM npc WHERE name = ?", (r_npc,))
                                        res_dialog_false = cur.fetchone()
                                        dialog = res_dialog_false[0].split('; ')
                                        with suppress(TelegramBadRequest):
                                            await call.message.edit_text(
                                                f"{dialog[random_dialog]} \n Вы ничего не получили.",
                                                reply_markup=fabric.paginator_dungeon()
                                            ) 
                                else:
                                    with suppress(TelegramBadRequest):
                                        await call.message.edit_text(
                                            f"Вы никого не обнаружили на своём пути.",
                                            reply_markup=fabric.paginator_dungeon()
                                        ) 
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
                            if battle == 0:
                                cur_event.execute("SELECT * FROM dungeon_event WHERE id = ?", (random.randint(1, 2),))
                                result_event = cur_event.fetchone()
                                random_ = random.randint(1, min(3, len(result_event)-1))
                                event = result_event[random_].split('; ')
                                _heal_false = result_safe[2]
                                proxy_list = ["116.203.28.43:80", "198.176.56.42:80", "51.75.122.80:80"]
                                random_proxy = random.choice(proxy_list)
                                request_gpt = "Сочени отрицательное событие от первого лица игрока который встречает что-то или кого-то и теряет уровень здоровье. Локация лес. На русском языке. Аудитория взрослая от 18 лет"
                                if event[0] == 'false':
                                    _heal_info = random.randint(1, 70)
                                    _heal_false_up = _heal_false - _heal_info
                                    response = None
                                    cur_safe.execute("UPDATE dungeon_safe SET heal = ? WHERE name = ?", (_heal_false_up, call.from_user.id,))
                                    db.commit()
                                    cur_safe.execute("SELECT * FROM dungeon_safe WHERE name = ?", (call.from_user.id,))
                                    result_safe = cur_safe.fetchone()
                                    try:
                                        response = await g4f.ChatCompletion.create_async(
                                            model=g4f.models.gpt_4,
                                            messages=[{"role": "user", "content": request_gpt}],
                                        )
                                        with suppress(TelegramBadRequest):
                                            await call.message.edit_text(
                                                f"{response} \n Вы потеряли {_heal_info} \n Ваш уровень здоровья {result_safe[2]}",
                                                reply_markup=fabric.paginator_dungeon()
                                            ) 
                                    except Exception as e:
                                        try:
                                            response = await g4f.ChatCompletion.create_async(
                                                model=g4f.models.default,
                                                messages=[{"role": "user", "content": request_gpt}],
                                            )
                                            with suppress(TelegramBadRequest):
                                                await call.message.edit_text(
                                                    f"{response} \n Вы потеряли {_heal_info} \n Ваш уровень здоровья {result_safe[2]}",
                                                    reply_markup=fabric.paginator_dungeon()
                                                )
                                        except Exception as e:
                                            try:
                                                response = await g4f.ChatCompletion.create_async(
                                                    model=g4f.models.gpt_35_turbo,
                                                    messages=[{"role": "user", "content": request_gpt}],
                                                )
                                                with suppress(TelegramBadRequest):
                                                    await call.message.edit_text(
                                                        f"{response} \n Вы потеряли {_heal_info} \n Ваш уровень здоровья {result_safe[2]}",
                                                        reply_markup=fabric.paginator_dungeon()
                                                    )
                                            except Exception as e: 
                                                try:
                                                    response = await g4f.ChatCompletion.create_async(
                                                        model=g4f.models.llama2_70b,
                                                        messages=[{"role": "user", "content": request_gpt}],
                                                    )
                                                    with suppress(TelegramBadRequest):
                                                        await call.message.edit_text(
                                                            f"{response} \n Вы потеряли {_heal_info} \n Ваш уровень здоровья {result_safe[2]}",
                                                            reply_markup=fabric.paginator_dungeon()
                                                        )
                                                except Exception as e:
                                                    with suppress(TelegramBadRequest):
                                                        await call.message.edit_text(
                                                            f"{event[1]} \n Вы потеряли {_heal_info} \n Ваш уровень здоровья {result_safe[2]}",
                                                            reply_markup=fabric.paginator_dungeon()
                                                        ) 
                                    if response == '' or response == None:
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
                                        try:
                                            response = await g4f.ChatCompletion.create_async(
                                                model=g4f.models.gpt_4,
                                                messages=[{"role": "user", "content": "Составь положительное событие от первого лица на русском языке когда игрок встречает что-то или кого-то и получает предмет но сам предмет не называй. Локация лес. Аудитория взрослая от 18 лет. Без примечаний."}],
                                            )
                                            with suppress(TelegramBadRequest):
                                                await call.message.edit_text(
                                                    f"{response} \n Вы нашли {random_element}",
                                                    reply_markup=fabric.paginator_dungeon()
                                                )
                                        except Exception as e:
                                            try:
                                                response = await g4f.ChatCompletion.create_async(
                                                    model=g4f.models.gpt_35_turbo_16k,
                                                    messages=[{"role": "user", "content": "Составь положительное событие от первого лица когда игрок встречает что-то или кого-то и получает предмет но сам предмет не называй. Локация лес. Аудитория взрослая от 18 лет. Без примечаний."}],
                                                )
                                                with suppress(TelegramBadRequest):
                                                    await call.message.edit_text(
                                                        f"{response} \n Вы нашли {random_element}",
                                                        reply_markup=fabric.paginator_dungeon()
                                                    ) 
                                            except Exception as e:
                                                try:
                                                    response = await g4f.ChatCompletion.create_async(
                                                        model=g4f.models.gpt_4,
                                                        messages=[{"role": "user", "content": "Составь положительное событие от первого лица когда игрок встречает что-то или кого-то и получает предмет но сам предмет не называй. Локация лес. Аудитория взрослая от 18 лет. Без примечаний."}],
                                                        proxy="http://74.48.78.52:80"
                                                    )
                                                    with suppress(TelegramBadRequest):
                                                        await call.message.edit_text(
                                                            f"{response} \n Вы нашли {random_element}",
                                                            reply_markup=fabric.paginator_dungeon()
                                                        ) 
                                                except Exception as e:
                                                    try:
                                                        response = await g4f.ChatCompletion.create_async(
                                                            model=g4f.models.llama2_70b,
                                                            messages=[{"role": "user", "content": "Составь положительное событие от первого лица когда игрок встречает что-то или кого-то и получает предмет но сам предмет не называй. Локация лес. Аудитория взрослая от 18 лет. Без примечаний."}],
                                                        )
                                                        with suppress(TelegramBadRequest):
                                                            await call.message.edit_text(
                                                                f"{response} \n Вы нашли {random_element}",
                                                                reply_markup=fabric.paginator_dungeon()
                                                            ) 
                                                    except Exception as e:
                                                        with suppress(TelegramBadRequest):
                                                            await call.message.edit_text(
                                                                f"{event[1]} \n Вы нашли {random_element}",
                                                                reply_markup=fabric.paginator_dungeon()
                                                            ) 
                                        if response == '' or response == None:
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
                        cur.execute("SELECT heal FROM dungeon_safe WHERE name = ?", (call.from_user.id,))
                        res_heal = cur.fetchone()
                        with suppress(TelegramBadRequest):
                            await call.message.edit_text(
                                f"Вы восстановили {r_heal} здоровья.\n Ваш уровень здоровья составляет: {res_heal[0]}",
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