from aiogram import Router, F
from aiogram.types import Message
from keyboards import reply, fabric
import sqlite3
from aiogram.enums import ChatAction
from aiogram import types

router = Router()
@router.message(F.text.lower().in_(["хай", "хелоу", "привит", "привет", "здравствуй"]))
async def greetings(message: Message):
    await message.answer("Привеет!")

# @router.message()
# async def echos(message: Message):
#     if message.sticker:
#         path_img = "image/fox.jpg"
#         await message.reply_sticker(sticker=message.sticker.file_id)
#         await message.reply_photo(photo=types.FSInputFile(path=path_img))
@router.message()
async def echo(message: Message):
    msg = message.text.lower()
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (message.from_user.id,))
    result = cur.fetchone()
    if msg == "начать игру":
        cur.execute(
            "UPDATE users SET active_game = ? WHERE name = ?" if result else "INSERT INTO users (name, active_game) VALUES (?, ?)",
            (1, message.from_user.id) if result else (message.from_user.id, 1)
        )
        db.commit()
        await message.answer("Вы начали игру")
    elif msg == 'меню игры':
        await message.answer('Вы открыли меню игры', reply_markup=reply.game)
    elif msg == 'о боте':
        await message.answer('Бот🦊 предоставляет маленькую новеллу с различными персонажами с которыми вы можете взаимодействовать. А также в бота встроен chatgpt 4!', reply_markup=reply.main)
    elif msg == 'выбрать персонажа':
        await message.answer('Выберите персонажа', reply_markup=fabric.paginator())
    elif msg == 'кто рядом':
        if result != None:
            if result[4] == 'true':
                if result[5] == 'Лес':
                    await message.answer(f"Прогуливаясь по локации '{result[5]}' вы встречаете", reply_markup=fabric.paginator_choose())
            else:
                await message.answer(f"При выборе персонажа нажмите подтвердить")
        else:
            await message.answer(f"Начните игру /start")
    elif msg == 'спустится в подземелье':
        if result != None:
            if result[4] == 'true':
                if result[5] == 'Лес':
                    path_img = "image/forest.gif"
                    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
                    await message.reply_animation(animation=types.FSInputFile(path=path_img))
                    await message.answer(f"Вы входите в подземелье Леса", reply_markup=fabric.paginator_dungeon())
            else:
                await message.answer(f"При выборе персонажа нажмите подтвердить")
        else:
            await message.answer(f"Начните игру /start")
    elif msg == 'статистика':
        if result != None:
            if result[4] == 'true':
                cur.execute("SELECT * FROM dungeon_safe WHERE name = ?", (message.from_user.id,))
                result_dangoen = cur.fetchone()
                cur.execute("SELECT relationship, relationship_npc FROM users WHERE name = ?", (message.from_user.id,))
                result_u = cur.fetchone()
                cur.execute("SELECT name_npc, mood, love FROM action_player_npc WHERE name = ?", (message.from_user.id,))
                all_npcs = cur.fetchall()
                answer_text = f"Ваш персонаж: {result[3]}\nВаши предметы: {result[8]}\nВаш уровень здоровья:{result_dangoen[2]}\n\n**Список персонажей с кем вы контактировали и их доверие:**\n"
                if all_npcs:
                    for npc in all_npcs:
                        answer_text += f"-{npc[0]} доверие-{npc[1]} романтическая связь-{npc[2]}\n"
                else:
                    answer_text += "- Нет активных NPC\n"
                if result_u[0] == 'true':
                    answer_text += f"-Вы в отношениях с {result_u[1]} \n"
                await message.answer(answer_text)
            else:
                await message.answer(f"При выборе персонажа нажмите подтвердить")
        else:
            await message.answer(f"Начните игру /start")