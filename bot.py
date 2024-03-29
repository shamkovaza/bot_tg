import asyncio
from aiogram import Bot, Dispatcher, Router
from handler import commands, message, chatgpt, sendphoto
from callback import pagination, choose_npc, action_ch, dyngeon, rem_bf
import os
from aiohttp import BasicAuth
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
load_dotenv()

async def main():
    bot = Bot(os.getenv('TOKEN_API'), parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        commands.router,
        pagination.router,
        choose_npc.router,
        action_ch.router,
        dyngeon.router,
        rem_bf.router,
        chatgpt.router,
        sendphoto.router,
        message.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())