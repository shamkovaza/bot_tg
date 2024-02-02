import asyncio
from aiogram import Bot, Dispatcher, Router
from handler import commands, message
from callback import pagination, choose_npc, action_ch, dyngeon
import os
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
        message.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())