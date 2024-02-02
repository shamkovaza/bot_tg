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