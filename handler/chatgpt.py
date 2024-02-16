from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import g4f
from utils.state import Form
from aiogram.enums import ChatAction
import random
import asyncio
import sqlite3
import curl_cffi

router = Router()

async def run_provider_false(formatted_text):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            proxy="http://5191.243.46.30:43241",
            messages=[{"role": "user", "content": formatted_text[0]}],
        )
        print(response)
    except Exception as e:
        print(e)

@router.message(Command("chatgpt"))
async def fill_profile(message: Message, state: FSMContext):
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    cur.execute("SELECT gpt FROM users WHERE name = ?", (message.from_user.id,))
    result = cur.fetchone()
    if result is None:
        await message.answer(f"Для этой функции отправте пожалуйста 'Начать игру' чтобы бот смог вас зарегестрировать и попытайтесь снова.")
    if result[0] == 'true':
        await state.set_state(Form.text)
        await message.answer(
            "Наш пушистый бот 🦊 использует модель GPT-4, GPT-3.5, Лама, из разных источников.\n Введите запрос:"
        )
        cur.execute("UPDATE users SET gpt = ? WHERE name = ?", ('false', message.from_user.id,))
        db.commit()
    else:
        await message.answer("Ваш запрос обробатывается.")
    db.close()
    
@router.message(Form.text)
async def form_text(message: Message, state: FSMContext):
    db = sqlite3.connect('data/mifoda.by.db')
    cur = db.cursor()
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    formatted_text = []
    for key, value in data.items():
        formatted_text.append(f"{value}")
    proxy_list = ["116.203.28.43:80", "198.176.56.42:80", "51.75.122.80:80"]
    random_proxy = random.choice(proxy_list)
    try:
        asyncio.run(run_provider_false(formatted_text))
    except Exception as e:
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": "Привет"}]
            ) 
            await message.answer(response)
            cur.execute("UPDATE users SET gpt = ? WHERE name = ?", ('true', message.from_user.id,))
            db.commit()
        except Exception as e:
            try:
                response = await g4f.ChatCompletion.create_async(
                    model=g4f.models.gpt_35_turbo,
                    messages=[{"role": "user", "content": formatted_text[0]}],
                ) 
                await message.answer(response)
                cur.execute("UPDATE users SET gpt = ? WHERE name = ?", ('true', message.from_user.id,))
                db.commit()
            except Exception as e:
                try:
                    response = await g4f.ChatCompletion.create_async(
                        model=g4f.models.llama2_70b,
                        messages=[{"role": "user", "content": formatted_text[0]}],
                    ) 
                    await message.answer(response)
                    cur.execute("UPDATE users SET gpt = ? WHERE name = ?", ('true', message.from_user.id,))
                    db.commit()
                except Exception as e:
                    try:
                        response = await g4f.ChatCompletion.create_async(
                            model=g4f.models.lzlv_70b,
                            messages=[{"role": "user", "content": formatted_text[0]}],
                        ) 
                        await message.answer(response)
                        cur.execute("UPDATE users SET gpt = ? WHERE name = ?", ('true', message.from_user.id,))
                        db.commit()  
                    except Exception as e:
                        try:
                            response = await g4f.ChatCompletion.create_async(
                                model=g4f.models.bard,
                                messages=[{"role": "user", "content": formatted_text[0]}],
                            ) 
                            await message.answer(response)
                            cur.execute("UPDATE users SET gpt = ? WHERE name = ?", ('true', message.from_user.id,))
                            db.commit()  
                        except Exception as e:
                            print(e)
                            await message.answer(f"Произошла ошибка, возможно из-за высокой нагрузки, повторите позже.")
                            cur.execute("UPDATE users SET gpt = ? WHERE name = ?", ('true', message.from_user.id,))
                            db.commit()
    db.close()
