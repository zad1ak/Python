import asyncio
from aiogram import Bot, Dispatcher

from handlers import router

async def main():
    bot = Bot(token='7826461419:AAGlv0FxWTfxogCWh31od4gen8CBUuzMveA')
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__ main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')    