import asyncio
import logging
import os
import aiohttp
import db

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()



logging.basicConfig(level=logging.INFO)
key = os.getenv('BOT_TOKEN')
bot = Bot(token=key)


dp = Dispatcher()





@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('привет хочешь курс валют тогда напиши usd')


@dp.message(F.text == 'usd')
async def c_start(message: types.Message):
        db.update_state(message.from_user.id, 'wait_amount')
        await message.answer('теперь веди число')


@dp.message()
async def c_current(message: types.Message):
    try:
        current=db.get_state(message.from_user.id)
        if current == 'wait_amount':
            amount = float(message.text)
            money = await get_usd_rate()
            result=amount * money
            await message.answer(f'нынешный курс {money}, вы получите {result:,.0f}')
            db.update_state(message.from_user.id,'')
    except ValueError:
        await message.answer('Введи число')


async def get_usd_rate():
    url = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            for usd in data:
                if usd['Ccy']== 'USD':
                    return float(usd['Rate'])

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    db.init_db()
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    asyncio.run(main())
