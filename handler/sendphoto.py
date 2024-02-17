import logging
import asyncio
from contextlib import suppress
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
import random
from aiogram.exceptions import TelegramBadRequest
from keyboards import reply
from aiogram import Router
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from aiogram.enums import ChatAction
from aiogram import types

router = Router()

async def login_session(username, password):
    login_url = 'https://www.furaffinity.net/login'
    session = requests.Session()
    payload = {
        'username': username,
        'password': password
    }
    response = session.post(login_url, data=payload)
    return session

async def download_image(url, folder_path, session):
    response = session.get(url)
    os.makedirs(folder_path, exist_ok=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    img = soup.find('img', id='submissionImg')
    
    if img:
        img_url = img.get('data-preview-src') or img.get('src')
        
        if img_url:
            img_url = urljoin(url, img_url)
            img_data = session.get(img_url).content
            with open(os.path.join(folder_path, "image.jpg"), 'wb') as f:
                f.write(img_data)
            
            print("Изображение успешно загружено!")
            return True
        else:
            print("URL изображения не найден.")
    else:
        print("Тег <img> с id='submissionImg' не найден.")


@router.message(Command("photo"))
async def fill_profile(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    username = ''
    password = ''
    folder_path = 'images'

    session = await login_session(username, password)
    if session:
        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            key = random.randrange(55500000, 55599999)
            url = f"https://www.furaffinity.net/view/{key}/"  
            if await download_image(url, folder_path, session):
                path_img = "images/image.jpg"
                await message.reply_photo(photo=types.FSInputFile(path=path_img))
                break 
            else:
                attempts += 1
        else:
            await message.answer(f"Не удалось найти изображение после {max_attempts} попыток.")